# gemini_ai.py
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import config
from speech_processing import speak_with_interruption

vertexai.init(project=config.PROJECT_ID, location=config.REGION)
generative_model = GenerativeModel("gemini-1.5-pro-002")

# Define wake words as a constant for easy maintenance
WAKE_WORDS = ["gemini", "gemini wake up"]

def query_gemini(user_query):
    """
    Process queries with wake word detection.
    Only responds if the query contains a wake word.
    Args:
        user_query (str): The voice input from user
    Returns:
        bool: True if query was processed, False if no wake word
    """
    lower_query = user_query.lower()
    
    # Check for wake word
    if not any(word in lower_query for word in WAKE_WORDS):
        return False
        
    # Clean query by removing wake words
    clean_query = lower_query
    for word in WAKE_WORDS:
        clean_query = clean_query.replace(word, "").strip()
    
# Only process if there's a query after removing wake word
    if clean_query:
        response = generative_model.generate_content([clean_query])
        if response:
            response_text = response.candidates[0].content.text.strip()
            speak_with_interruption(response_text)
            return True
        else:
            print("No response received from Gemini.")
            return False
    return False