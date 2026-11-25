
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


class GeminiService:
    def __init__(self):
        if not API_KEY:
            raise ValueError("Gemini API key not found in .env file.")

        http_options = types.HttpOptions(timeout=60000)

        self.client = genai.Client(
            api_key=API_KEY,
            http_options=http_options
        )

        self.model = MODEL_NAME

    def generate_response(self, prompt):

        max_attempts = 2

        for attempt in range(max_attempts):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if response.text:
                    return response.text

                return "Gemini returned an empty response."

            except Exception as error:

                error_message = str(error).lower()

                temporary_errors = [
                    "503",
                    "504",
                    "429",
                    "timeout",
                    "timed out",
                    "deadline_exceeded",
                    "unavailable",
                    "high demand"
                ]

                is_temporary = any(
                    item in error_message
                    for item in temporary_errors
                )

                if is_temporary and attempt < max_attempts - 1:
                    print("Gemini temporarily busy. Retrying...")
                    time.sleep(3)
                    continue

                if is_temporary:
                    return (
                        "Gemini AI is temporarily busy. "
                        "Please try again in a few moments."
                    )

                return f"Gemini Error: {error}"

        return "Unable to generate a response. Please try again."


if __name__ == "__main__":
    try:
        gemini = GeminiService()

        print("Gemini Service Initialized Successfully!")

        answer = gemini.generate_response(
            "Introduce yourself as an AI Travel Assistant in two sentences."
        )

        print("\nGemini Response:")
        print(answer)

    except Exception as error:
        print("Gemini Service Initialization Failed:", error)
