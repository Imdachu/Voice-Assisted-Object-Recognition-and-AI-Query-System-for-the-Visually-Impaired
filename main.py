import cv2
from object_recognition import detect_objects, categorize_objects, announce_objects, handle_object_query
from speech_processing import get_voice_input, process_voice_command, start_listening_thread
from gemini_ai import query_gemini
import config  # Import global mode state and switch function
import time


def main():
    """
    Main function running the video capture and processing loop.
    Handles both continuous and on-demand modes for object recognitions
    and voice interactions.
    """
    # Initialize video capture
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        print("Error: Could not open video capture device")
        return

    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Only perform object detection if recognition is enabled
            width = frame.shape[1]  # Default width if detection is disabled
            if config.recognition_enabled:
                result = detect_objects(frame)
                if result is not None:
                    width = result

            else:
                # Add visual feedback when recognition is disabled
                cv2.putText(
                    frame,
                    "Object Recognition Disabled",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),  # Red color
                    2
                )

            # Add Gemini disabled visual feedback
            if not config.gemini_enabled:
                cv2.putText(
                    frame,
                    "Gemini AI Disabled",
                    (10, 60),  # Positioned below object recognition text
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),  # Blue color
                    2
                )

            if config.current_mode == "continuous":
                # Start background listener for mode switching
                start_listening_thread()
                
                # Continuous object detection and announcement
                while config.current_mode == "continuous":
                    if config.recognition_enabled:
                        left, middle, right = categorize_objects(width)
                        announce_objects(left, middle, right)

                    else:
                        # Small delay to prevent CPU overload when disabled
                        time.sleep(0.1)

            else:  # On-Demand Mode
                # Get voice input from user
                user_query = get_voice_input()
                if user_query:
                    # Check for mode switching commands
                    process_voice_command(user_query)
                    
                    if config.current_mode == "on_demand" and config.recognition_enabled:
                        # Only process object queries if recognition is enabled
                        if not handle_object_query(user_query, width):
                            # If not an object query and Gemini is enabled, try Gemini
                            if config.gemini_enabled:
                                query_gemini(user_query)
                            

                    elif config.current_mode == "on_demand" and not config.recognition_enabled:
                        # Try Gemini if object recognition is disabled and Gemini is enabled
                        if config.gemini_enabled:
                            query_gemini(user_query)
                        
            

            # Display video feed
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        # Clean up resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()