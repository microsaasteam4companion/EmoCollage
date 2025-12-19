import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

print(f"CWD: {os.getcwd()}")
script_path = Path(__file__).resolve()
env_path = script_path.parent / '.env'
print(f"Looking for .env at: {env_path}")

if env_path.exists():
    print("File exists.")
    with open(env_path, 'r') as f:
        content = f.read()
        print(f"File content length: {len(content)}")
        print(f"First 20 chars: {content[:20]!r}")
else:
    print("File DOES NOT exist.")

print("Loading dotenv...")
load_dotenv(dotenv_path=env_path)
key = os.getenv("GEMINI_API_KEY")

if key:
    print(f"Key found (length: {len(key)})")
    genai.configure(api_key=key)
    print("Listing available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Found model: {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
else:
    print("KEY IS NONE")
