import os
from dotenv import load_dotenv
from ai.gemini_client import GeminiClient

# Load API key from .env if present
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in environment. Please set it in .env file.")
else:
    try:
        client = GeminiClient(api_key)
        print("✅ GeminiClient initialized successfully.")
        # We don't necessarily need to call the API here to verify imports,
        # but the initialization confirms google.generativeai and ai.prompts are loaded.
    except Exception as e:
        print(f"❌ Error during GeminiClient initialization: {e}")
