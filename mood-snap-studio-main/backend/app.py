import os
import io
import json
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from pathlib import Path

# =========================
# ENV SETUP
# =========================
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)

# =========================
# GEMINI MODEL
# =========================
model = genai.GenerativeModel("gemini-flash-latest")

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="Mood Snap Studio – AI Brain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Mood Snap AI Brain Running (Gemini Powered)"}

# =========================
# IMAGE ENGINE IMPORTS
# =========================
from collage_engine import create_collage_from_analysis

# =========================
# MAIN ENDPOINT
# =========================
@app.post("/analyze-emotion")
async def analyze_emotion(
    files: list[UploadFile] = File(...),
    theme: str = Form("magazine"),
    user_prompt: str = Form("")
):
    print(f"--- STARTING STUDIO REQUEST [{theme}] with {len(files)} photos ---")

    try:
        # Read all uploaded files
        photo_bytes_list = []
        for file in files:
            contents = await file.read()
            photo_bytes_list.append(contents)
            print(f"LOG: Photo {len(photo_bytes_list)} - {len(contents)} bytes")

        # STEP 1: Gemini analysis (using first photo as representative)
        first_image = Image.open(io.BytesIO(photo_bytes_list[0]))

        prompt = f"""
You are an elite, world-class Creative Director (Vogue/GQ level).

Analyze the image and return a STRICT JSON object only.

SCHEMA:
{{
  "dominantEmotion": "ONE strong word",
  "vibeDescription": "6-word editorial headline",
  "collageStyle": "scrapbook|magazine|moodboard|filmstrip|doodle",
  "emotions": ["3 words"],
  "colorPalette": ["5 hex codes from the image"]
}}

Theme: {theme}
User Context: {user_prompt}

IMPORTANT: For collageStyle, choose:
- "scrapbook" for casual, memory-focused vibes
- "magazine" for fashion, editorial, professional
- "moodboard" for aesthetic, Pinterest-style, inspiration
- "filmstrip" for sequences, stories, cinematic
- "doodle" for fun, playful, youthful energy
"""

        response = model.generate_content([prompt, first_image])
        raw_text = response.text.strip().replace("```json", "").replace("```", "")

        try:
            gemini_json = json.loads(raw_text)
        except Exception as parse_error:
            print(f"JSON parse error: {parse_error}")
            gemini_json = {
                "dominantEmotion": "Ethereal",
                "vibeDescription": "Visual story in motion",
                "collageStyle": theme if theme in ["scrapbook", "magazine", "moodboard", "filmstrip", "doodle"] else "moodboard",
                "emotions": ["Creative", "Soft", "Elegant"],
                "colorPalette": ["#F5F5F5", "#E0E0E0", "#9E9E9E", "#7D7D7D", "#5A5A5A"]
            }

        print(f"Analysis: {gemini_json}")

        # STEP 2: Create collage using the engine
        print("Creating collage...")
        collage_bytes = create_collage_from_analysis(photo_bytes_list, gemini_json)
        
        # STEP 3: Encode collage to base64
        collage_base64 = base64.b64encode(collage_bytes).decode()

        print("--- REQUEST SUCCESSFUL ---")

        return {
            "analysis": gemini_json,
            "collage_image": f"data:image/png;base64,{collage_base64}",
            "enhanced_image": None,  # Deprecated - now using collage_image
            "sticker_image": None    # Deprecated
        }

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "analysis": {
                "dominantEmotion": "Calm",
                "vibeDescription": "Minimal visual fallback",
                "collageStyle": "moodboard",
                "emotions": ["Calm", "Neutral", "Soft"],
                "colorPalette": ["#F5F5F5", "#E0E0E0", "#9E9E9E", "#7D7D7D", "#5A5A5A"]
            },
            "collage_image": None,
            "enhanced_image": None,
            "sticker_image": None,
            "error": str(e)
        }
