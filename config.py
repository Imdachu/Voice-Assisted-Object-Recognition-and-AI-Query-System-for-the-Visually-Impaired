# config.py

current_mode = "on_demand"  # Default mode
recognition_enabled = True  # Default recognition state
gemini_enabled = True  # New variable for Gemini state

def switch_mode(new_mode):
    """Update the current mode (on_demand <-> continuous)"""
    global current_mode
    current_mode = new_mode
    print(f"Mode switched to: {current_mode}")


def toggle_recognition(enabled):
    """Toggle object recognition state"""
    global recognition_enabled
    recognition_enabled = enabled
    print(f"Object recognition {'enabled' if enabled else 'disabled'}")

def toggle_gemini(enabled):
    """Toggle Gemini AI state"""
    global gemini_enabled
    gemini_enabled = enabled
    print(f"Gemini AI {'enabled' if enabled else 'disabled'}")


    # Project ID and Region for Vertex AI
PROJECT_ID = "concise-dolphin-441609-p9"
REGION = "us-central1"
