import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Securely load API key
api_key = os.getenv("GEMINI_API_KEY")  # Ensure key is named correctly in .env
if not api_key:
    raise ValueError("API key not found. Make sure it is set in the .env file.")

# Configure the Gemini API
genai.configure(api_key=api_key)

# Generation configuration for shorter, chat-like responses
generation_config = {
    "temperature": 0.6,  # Keeps responses stable but still natural
    "top_p": 0.8,
    "top_k": 30,
    "max_output_tokens": 50,  # Limits response length
    "response_mime_type": "text/plain",
}

# Initialize the Gemini model for Dr. Smith (now more casual)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session with a friendly, non-formal introduction
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": ["You are Dr. Smith, a friendly and supportive chatbot. Keep responses short and engaging."],
        },
        {
            "role": "model",
            "parts": ["Hey! I'm Dr. Smith, here to chat. What's on your mind?"],
        },
    ]
)

# Function to check for predefined responses
def get_special_response(user_message):
    """Returns predefined responses for identity-related questions."""
    user_message = user_message.lower().strip()

    responses = {
        "who are you": "I'm Dr. Smith, your virtual friend here to chat and support you.",
        "what is your name": "I'm Dr. Smith, always here to listen.",
        "who created you": "I was developed by **Team Citronix**, passionate about AI mental health support.",
        "who developed you": "Team Citronix built me to help people feel heard and supported."
    }

    for key, response in responses.items():
        if key in user_message:
            return response

    return None  # Return None if no predefined response is needed

# Function to process user input dynamically
def chat_with_bot(user_message):
    """Handles user input and generates a response from Dr. Smith."""
    user_message = user_message.strip()

    # Check for predefined responses
    special_response = get_special_response(user_message)
    if special_response:
        return special_response

    # Get response from Gemini API
    response = chat_session.send_message(user_message)

    # Ensure response is valid
    if response and response.text:
        return response.text.strip().split(".")[0] + "."  # Keep only the first sentence for brevity
    
    return "I'm here for you. What's up?"
