
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key:
    print("ERROR: Gemini API key not found in .env file.")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model_name,
            contents="You are an AI Travel Assistant. Introduce yourself in two sentences."
        )

        print("\nSUCCESS! Gemini AI Connected.")
        print("\nGemini Response:")
        print(response.text)

    except Exception as e:
        print("\nGemini Connection Failed.")
        print("Error:", e)
