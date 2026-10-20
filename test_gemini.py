import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

if not api_key:
    raise SystemExit(
        "ERROR: GEMINI_API_KEY was not found in your .env file."
    )

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly: Gemini API connection successful!"
    )

    print("\nGemini response:")
    print(response.text)

except Exception as exc:
    print("\nGemini API request failed.")
    print("Error:", exc)