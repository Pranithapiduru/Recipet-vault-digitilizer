import google.generativeai as genai # type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No GEMINI_API_KEY found in .env file.")
else:
    print(f"✅ Found API Key (Length: {len(str(api_key))})")
    try:
        genai.configure(api_key=api_key)
        print("Listing available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
