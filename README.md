# Smart Visual Assistant

## Project Summary
Smart Visual Assistant is an AI-powered desktop application that helps visually impaired users interact with their environment. It combines real-time object recognition (using YOLOv4-tiny) and voice-based AI queries (using Google Gemini AI and Vosk/Google Speech Recognition) for a fully hands-free experience.


---
📦 To run or test this project, simply extract the ZIP file and launch the executable.  (https://drive.google.com/file/d/1LQpHb-XYGv9MUabUrxw9w5zVah6klQdG/view?usp=drive_link)
📘 For detailed instructions, please refer to the included User Guide

### **Why This Project?**  
To create a **practical, real-world solution** that empowers visually impaired individuals to **interact with both their surroundings and AI** in a seamless way.  

So, I combined:  
✅ **Computer Vision** (Object recognition with YOLOv4)  
✅ **AI-Powered Query System** (Google Gemini AI)  
✅ **Voice-Controlled Interaction** (Speech recognition & response control)  

Now, users can not only **identify objects around them** but also **ask general AI queries just like anyone else.**  

---

## Features
- Real-time object detection via webcam
- Voice-activated control and feedback
- AI-powered question answering (Google Gemini AI)
- Two operation modes: On-Demand and Continuous
- Interruptible speech responses
- Works offline (Vosk) and online (Google Speech Recognition)

## System Requirements
- **Hardware:**
  - Windows 10+ PC or laptop
  - Webcam
  - Microphone and speakers/headphones
- **Software:**
  - Python 3.7+
  - Required Python packages (see below)

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

## Installation Guide

### 1. Install Python and Required Packages
- Download and install Python 3.7 or newer from [python.org](https://www.python.org/downloads/).
- Open a terminal/command prompt in the project directory and run:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Download YOLOv4-tiny Model Files
- **yolov4-tiny.weights:**
  - Download from [official YOLO website](https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov4-tiny.weights)
- **yolov4-tiny.cfg:**
  - Download from [here](https://github.com/AlexeyAB/darknet/blob/master/cfg/yolov4-tiny.cfg) (right-click > Save As)
- **coco.names:**
  - Download from [here](https://github.com/pjreddie/darknet/blob/master/data/coco.names) (right-click > Save As)
- Place all three files in the project root directory (same folder as main.py).

### 3. Download and Set Up Vosk Speech Recognition Model
- Visit the [Vosk models page](https://alphacephei.com/vosk/models)
- Download a small English model, e.g., `vosk-model-small-en-us-0.15.zip`
- Extract the zip file. You should get a folder like `vosk-model-small-en-us-0.15`
- Place this folder inside the `model/` directory in your project (so you have `model/vosk-model-small-en-us-0.15`)

### 4. (Optional) Google Gemini AI Setup
- If you want to use Gemini AI features, set up Google Cloud credentials:
  - Follow [Google Cloud authentication guide](https://cloud.google.com/docs/authentication/getting-started)
  - Enable Gemini/Vertex AI API in your Google Cloud project
  - Download your credentials JSON and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to its path

## How to Run the Application

### A. From Source (Python)
- Open a terminal in the project directory and run:
  ```bash
  python main.py
  ```

### B. Using the Executable (.exe)
- If you have a pre-built executable (e.g., `smart-visual.exe` in the `dist/` folder):
  - Double-click the `.exe` file to launch the application

## File and Folder Structure
```
project-root/
│── main.py
│── config.py
│── object_recognition.py
│── speech_processing.py
│── gemini_ai.py
│── yolov4-tiny.cfg
│── yolov4-tiny.weights
│── coco.names
│── requirements.txt
│── README.md
│── model/
│    └── vosk-model-small-en-us-0.15/  # (or similar)
```



## Troubleshooting
- **Missing Packages:** Run `pip install -r requirements.txt` again
- **Microphone/Camera Not Detected:** Check device connections and Windows settings
- **Model Not Found:** Ensure all model files are in the correct locations
- **Google Gemini AI Not Working:** Check your Google Cloud credentials and API setup
- **Permission Errors:** Try running the terminal or executable as administrator

---

For questions or support, please refer to the User Guide or contact the project maintainer.
