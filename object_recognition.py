import cv2
import numpy as np
import pyttsx3
import threading
from threading import Lock
from collections import deque
from config import current_mode
import sys
import os

# Initialize TTS engine
engine = pyttsx3.init()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load YOLOv4 model
net = cv2.dnn.readNet(resource_path("yolov4-tiny.weights"), resource_path("yolov4-tiny.cfg"))
with open(resource_path("coco.names"), "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

# Object tracker with thread safety and frame buffer
class ObjectTracker:
    def __init__(self, max_frames=5):
        self.recognized_objects = {}
        self.lock = Lock()
        self.frame_buffer = deque(maxlen=max_frames)  # Buffer for recent detections
    
    def update_objects(self, new_detections):
        with self.lock:
            self.frame_buffer.append(new_detections)
            # Merge detections from recent frames
            self.recognized_objects = {}
            for detections in self.frame_buffer:
                self.recognized_objects.update(detections)

object_tracker = ObjectTracker()

# Frame skipping and processing parameters
FRAME_SKIP = 3
frame_count = 0
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

# Define keywords for object location queries
LOCATION_KEYWORDS = {
    "left": ["left"],
    "middle": ["middle", "center"],
    "right": ["right"],
    "all": ["object", "objects", "nearby"]
}

def preprocess_frame(frame):
    """Optimize frame before detection"""
    blob = cv2.dnn.blobFromImage(
        frame, 
        1/255.0, 
        (416, 416),
        swapRB=True,
        crop=False
    )
    return blob

def detect_objects(frame):
    """Detect objects in a video frame using YOLOv4."""
    global frame_count
    frame_count += 1
    
    # Skip frames if needed
    if frame_count % FRAME_SKIP != 0:
        return frame.shape[1]
    
    height, width = frame.shape[:2]
    blob = preprocess_frame(frame)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    
    boxes = []
    confidences = []
    class_ids = []
    detected_objects = {}

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > CONFIDENCE_THRESHOLD:
                center_x, center_y, w, h = (detection[:4] * np.array([width, height, width, height])).astype("int")
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    
    if len(indices) > 0:
        for i in indices.flatten():
            label = str(classes[class_ids[i]])
            detected_objects[label] = {
                "position": (boxes[i][0], boxes[i][1]),
                "confidence": confidences[i]
            }
            
            # Draw bounding box and label
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    object_tracker.update_objects(detected_objects)
    return width

def categorize_objects(width):
    """Categorize detected objects into left, middle, and right sections."""
    left, middle, right = [], [], []
    with object_tracker.lock:
        for obj, data in object_tracker.recognized_objects.items():
            x, _ = data["position"]
            if x < width // 3:
                left.append(obj)
            elif x > 2 * width // 3:
                right.append(obj)
            else:
                middle.append(obj)
    return left, middle, right

def announce_objects(left, middle, right):
    """Announce all detected objects and their positions using text-to-speech."""
    response = f"Objects on the left: {', '.join(left) or 'None'}. "
    response += f"Objects in the middle: {', '.join(middle) or 'None'}. "
    response += f"Objects on the right: {', '.join(right) or 'None'}."
    engine.say(response)
    engine.runAndWait()

def handle_object_query(user_query, width):
    """Process keyword-based object recognition queries."""
    lower_query = user_query.lower()
    has_keywords = any(
        any(keyword in lower_query for keyword in keywords)
        for keywords in LOCATION_KEYWORDS.values()
    )
    
    if not has_keywords:
        return False
    
    left_objects, middle_objects, right_objects = categorize_objects(width)
    
    if any(keyword in lower_query for keyword in LOCATION_KEYWORDS["left"]):
        response = "Objects on the left: " + ", ".join(left_objects) + "." if left_objects else "No objects on the left."
    elif any(keyword in lower_query for keyword in LOCATION_KEYWORDS["middle"]):
        response = "Objects in the middle: " + ", ".join(middle_objects) + "." if middle_objects else "No objects in the middle."
    elif any(keyword in lower_query for keyword in LOCATION_KEYWORDS["right"]):
        response = "Objects on the right: " + ", ".join(right_objects) + "." if right_objects else "No objects on the right."
    else:
        response = (
            f"Objects on the left: {', '.join(left_objects) if left_objects else 'None'}. "
            f"Objects in the middle: {', '.join(middle_objects) if middle_objects else 'None'}. "
            f"Objects on the right: {', '.join(right_objects) if right_objects else 'None'}."
        )
    
    engine.say(response)
    engine.runAndWait()
    return True

# Main processing loop
def main():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        width = detect_objects(frame)
        cv2.imshow("Object Detection", frame)
        
        # Example query handling (replace with your actual input mechanism)
        if current_mode == "query":
            handle_object_query("What objects are on the left?", width)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()