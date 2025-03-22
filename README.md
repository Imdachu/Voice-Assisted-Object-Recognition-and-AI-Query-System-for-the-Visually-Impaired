# Voice-Assisted-Object-Recognition-and-AI-Query-System-for-the-Visually-Impaired(laptop based project)
A voice-assisted AI system for visually impaired users, combining YOLOv4 object detection and Google Gemini AI for real-time interaction. Users can recognize objects, ask AI queries, switch modes, and control responses via voice commands. Features on-demand &amp; continuous modes with interruptible responses for a seamless experience. 
Here's the updated project description and README with the additional content integrated:  

---



### **Why This Project?**  
To create a **practical, real-world solution** that empowers visually impaired individuals to **interact with both their surroundings and AI** in a seamless way.  

So, I combined:  
✅ **Computer Vision** (Object recognition with YOLOv4)  
✅ **AI-Powered Query System** (Google Gemini AI)  
✅ **Voice-Controlled Interaction** (Speech recognition & response control)  

Now, users can not only **identify objects around them** but also **ask general AI queries just like anyone else.**  

---

## **Key Features**  
- **Two Modes of Interaction**  
  - **On-Demand Mode**: Users receive feedback only when they ask.  
  - **Continuous Mode**: Provides real-time updates about surroundings.  
- **AI Query System** – Uses **Google Gemini AI** to answer general questions.  
- **Real-Time Object Detection** – Uses **YOLOv4** to detect objects in a live video feed.  
- **Speech Processing** – Supports **Google Speech Recognition** and **Vosk (offline mode)** for voice commands.  
- **Wake Word Detection** – Users can trigger AI with wake words like `"Gemini wake up"`.  
- **Interruptible Responses** – Users can **stop** AI responses anytime using voice commands.  

---

## **Installation Guide**  

### **Prerequisites**  
Make sure you have Python 3.x installed. Then, install the required libraries:  
```bash
pip install opencv-python numpy pyttsx3 vosk speechrecognition google-cloud-aiplatform
```

### **Setup Instructions**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/object-ai-assistant.git
   cd object-ai-assistant
   ```
2. Configure **Google Vertex AI** credentials for Gemini AI.  
3. Place **YOLOv4 model files** (`yolov4-tiny.weights`, `yolov4-tiny.cfg`, `coco.names`) inside the `object and face/` directory.  
4. Run the main script:  
   ```
   python main.py
   ```
   - Press `'q'` to quit the application.  

---

## **How It Works**  

### **1. Object Recognition**  
- The system continuously captures frames from the webcam.  
- **YOLOv4** detects and categorizes objects in real-time.  
- Object positions are classified as **left, middle, or right** for better spatial awareness.  
- The system **announces detected objects** using text-to-speech (TTS).  

### **2. AI-Powered Queries (Gemini AI Integration)**  
- Users can **ask general questions** by speaking wake words like `"Gemini wake up"`.  
- The system processes the query and **retrieves responses from Google Gemini AI**.  
- If the response is long, users can **interrupt it anytime with a stop command**.  

### **3. Voice Control & Mode Switching**  
- Users can **switch between on-demand and continuous modes** using voice commands.  
- Object recognition and AI query responses can be toggled on/off dynamically.  

---

## **File Structure**  
```
/object-ai-assistant
│── config.py              # Stores mode and feature toggles
│── main.py                # Main execution loop
│── object_recognition.py   # Handles object detection with YOLOv4
│── speech_processing.py    # Manages voice input and text-to-speech output
│── gemini_ai.py            # Handles AI-based responses via Gemini
│── object and face/        # YOLOv4 model files (weights, config, labels)
```

---

## **Example Voice Commands**  

| Command                     | Action Performed |
|-----------------------------|----------------|
| `"Gemini wake up, what is AI?"` | Calls Gemini AI for an answer. |
| `"Switch to next"` | Switches to continuous mode. |
| `"Switch to back"` | Switches to on-demand mode. |
| `"Start recognition"` | Enables object detection. |
| `"Stop recognition"` | Disables object detection. |
| `"Stop query"` | Stops Gemini AI responses. |

---

## **Future Enhancements**  
- ✅ **Multi-language support** for voice interactions.  
- ✅ Integration with **mobile devices** for accessibility.  
- ✅ More **natural language understanding** for AI responses.  

