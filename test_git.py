import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

if not api_key:
    raise SystemExit("GEMINI_API_KEY is missing from .env")

if not model:
    raise SystemExit("GEMINI_MODEL is missing from .env")

client = genai.Client(api_key=api_key)

try:
    print(f"Testing Gemini model: {model}")
    print("Sending request...")

    response = client.models.generate_content(
        model=model,
        contents=(
            "Explain how to create a GitHub repository from an "
            "existing local folder and push the files using Git. "
            "Give step-by-step Windows PowerShell commands."
        ),
    )

    print("\n--- GEMINI RESPONSE ---\n")
    print(response.text or "Gemini returned no text.")

except Exception as exc:
    print(f"\nRequest failed: {type(exc).__name__}: {exc}")