import os
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import logging
import time
import threading
import config
import pyttsx3
import sys


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize TTS engine with interruption support
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Adjust speech rate

# Initialize SpeechRecognition (Google API)
recognizer = sr.Recognizer()
mic = sr.Microphone()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Vosk Model (Offline)
# model = Model(r"B:\final_year\execute\model")  # Path to Vosk model
model_path = resource_path("model")

try:
    model = Model(model_path)
    vosk_recognizer = KaldiRecognizer(model, 16000)
except Exception as e:
    logger.error(f"Failed to initialize Vosk model: {e}")
    model = None
    vosk_recognizer = None


def chunk_text(text):
    """Split text into natural speaking chunks"""
    chunks = []
    current_chunk = []
    for word in text.split():
        current_chunk.append(word)
        if len(current_chunk) >= 12 or word[-1] in '.!?':
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks


def speak_with_interruption(text):
    """Speak text with interruption support"""
    stop_event = threading.Event()
    is_speaking = [True]  # Using a mutable list for thread-safe flag

    def background_listener():
        """Continuous background listener for stop commands"""
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                while is_speaking[0]:
                    try:
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=1)
                        interrupt_text = recognizer.recognize_google(audio).lower()
                        if any(kw in interrupt_text for kw in ["stop response", "cancel", "shut up","stop"]):
                            stop_event.set()
                            
                            print("\nInterruption detected!")
         
                            return  # Exit the listener thread
                    except (sr.WaitTimeoutError, sr.UnknownValueError):
                        continue
        except Exception as e:
            print(f"Listener error: {e}")


        # Start background listener thread
    listener_thread = threading.Thread(target=background_listener, daemon=True)
    listener_thread.start()

    # Split text into natural chunks
    chunks = chunk_text(text)

    try:
        for chunk in chunks:
            if stop_event.is_set():
                break
            engine.say(chunk)
            engine.runAndWait()
            time.sleep(0.1)  # Brief pause between chunks

        # Speak confirmation message after interruption is detected
        if stop_event.is_set():
            engine.say("okk i will stop")
            engine.runAndWait()

    except RuntimeError as e:
        print(f"Error in speech engine: {e}")

    finally:
        is_speaking[0] = False
        listener_thread.join()

def get_voice_input(prefer_online=True, timeout=10):
    if prefer_online:
        try:
            with sr.Microphone() as source:
                print("Listening (Google API)...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
                command = recognizer.recognize_google(audio).lower()
                print("User said (Google):", command)
                return command
        except sr.UnknownValueError:
            print("Google API: Sorry, could not understand.")
        except sr.RequestError:
            print("Google API: Request failed, switching to Vosk.")
        except sr.WaitTimeoutError:
            print("Google API: Listening timed out.")
        except Exception as e:
            print(f"Unexpected error with Google API: {e}")

    # If Google API fails or prefer_online=False, use Vosk
    return get_voice_input_vosk()

def get_voice_input_vosk():
    """
    Capture and return voice input using Vosk (offline) with continuous listening.
    """
    if not model or not vosk_recognizer:
        logger.error("Vosk model not initialized")
        return None

    pa = pyaudio.PyAudio()
    stream = None
    try:
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4096
        )
        stream.start_stream()
        
        print("Listening (Vosk) - Say something or press Ctrl+C to stop...")
        vosk_recognizer.Reset()  # Reset the recognizer before starting
        
        while True:
            try:
                data = stream.read(4096, exception_on_overflow=False)
                if vosk_recognizer.AcceptWaveform(data):
                    result = json.loads(vosk_recognizer.Result())
                    command = result.get("text", "").lower().strip()
                    if command:
                        print("User said (Vosk):", command)
                        return command
            except KeyboardInterrupt:
                print("\nListening stopped by user.")
                return None
            
    except Exception as e:
        logger.error(f"Vosk recognition error: {e}")
        return None
    finally:
        # Carefully check and close the stream
        if stream and stream.is_active():
            try:
                stream.stop_stream()
                stream.close()
            except Exception as e:
                logger.error(f"Error closing stream: {e}")
        pa.terminate()
        
 
def process_voice_command(command):
    """Process user voice commands to switch modes and provide voice feedback."""
    if "switch to back" in command:
        config.switch_mode("on_demand")
        engine.say("i will got to on demand mode")
        engine.runAndWait()
    elif "switch to next" in command:
        config.switch_mode("continuous")
        engine.say("now you are in continuous mode")
        engine.runAndWait()
    elif "stop recognition" in command:
        config.toggle_recognition(False)
        engine.say("Object recognition disabled")
        engine.runAndWait()
    elif "start recognition" in command:
        config.toggle_recognition(True)
        engine.say("Object recognition enabled")
        engine.runAndWait()
    elif "stop query" in command:
        config.toggle_gemini(False)
        engine.say("Gemini AI disabled")
        engine.runAndWait()
    elif "start query" in command:
        config.toggle_gemini(True)
        engine.say("Gemini AI enabled")
        engine.runAndWait()

def listen_for_mode_switch():
    """Continuously listen for the switch command in a background thread."""
    while True:
        command = get_voice_input()
        if command:
            process_voice_command(command)

def start_listening_thread():
    """Start a background thread for voice input in Continuous Mode."""
    thread = threading.Thread(target=listen_for_mode_switch, daemon=True)
    thread.start()