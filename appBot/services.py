import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Securely load API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure it is set in the .env file.")

# Configure Gemini API
genai.configure(api_key=api_key)

# Generation configuration for balanced responses
generation_config = {
    "temperature": 0.6,  
    "top_p": 0.8,
    "top_k": 30,
    "max_output_tokens": 80,  # Increased to ensure full responses
    "response_mime_type": "text/plain",
}

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session with a conversational tone
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["You are Dr. Smith, a friendly mental health chatbot. Keep responses supportive, concise, and engaging."],
        },
        {
            "role": "model",
            "parts": ["Hey! I'm Dr. Smith, here to chat and support you. How's your day going?"],
        },
    ]
)

# Function to check for predefined responses
def get_special_response(user_message):
    """Returns predefined responses for common identity-related questions."""
    user_message = user_message.lower().strip()

    responses = {
        "who are you": "I'm Dr. Smith, your AI mental health companion. I'm here to listen and support you.",
        "what is your name": "I'm Dr. Smith, always here to help!",
        "who created you": "I was developed by **Team Citronix**, focused on AI-powered mental health care.",
        "who developed you": "I was built by **Team Citronix** to provide emotional support and guidance.",
    }

    for key, response in responses.items():
        if key in user_message:
            return response

    return None  # No predefined response, let AI generate one

# Function to process user input dynamically
def chat_with_bot(user_message):
    """Handles user input and generates a response from Dr. Smith."""
    user_message = user_message.strip()

    # Check for predefined responses
    special_response = get_special_response(user_message)
    if special_response:
        return special_response

    # Get AI-generated response
    response = chat_session.send_message(user_message)

    # Ensure response is valid and not too short
    if response and response.text and len(response.text.strip()) > 10:
        return response.text.strip()
    
    return "I'm here for you. What's on your mind?"
