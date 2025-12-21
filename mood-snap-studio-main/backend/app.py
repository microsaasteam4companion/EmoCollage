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
    # Sanity check for libraries
    status = {"status": "Mood Snap AI Brain Running"}
    try:
        import cv2
        import rembg
        import PIL
        status["libraries"] = "✅ Expert Engine Loaded"
    except ImportError as e:
        status["libraries"] = f"❌ Missing Library: {e}"
        print(f"CRITICAL WARNING: {e}. Please run 'pip install -r requirements.txt'")
    
    return status

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

        # STEP 1: Gemini analysis (with surgical fallback for rate limits)
        first_image = Image.open(io.BytesIO(photo_bytes_list[0]))
        prompt = f"""
AS AN ELITE CREATIVE DIRECTOR:
Analyze this image. Return STRICT JSON: {{ "dominantEmotion": "", "vibeDescription": "", "collageStyle": "{theme}", "emotions": [], "colorPalette": [] }}
Theme: {theme}
"""
        try:
            print("LOG: Requesting AI Analysis (Gemini)...")
            response = model.generate_content([prompt, first_image])
            # If AI is blocked, accessing .text will raise an exception
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            gemini_json = json.loads(raw_text)
            print(f"LOG: AI Analysis Success -> {gemini_json.get('dominantEmotion', 'Unknown')}")
        except Exception as ai_err:
            print(f"WARNING: AI Studio Busy or Quota Limit Hit. Activating Artisanal Fallback.")
            # We don't fail, we just use a premium pre-defined vibe
            gemini_json = {
                "dominantEmotion": "Timeless",
                "vibeDescription": "A curated visual story by Mood Snap",
                "collageStyle": theme if theme in ["scrapbook", "magazine", "moodboard", "filmstrip", "doodle"] else "magazine",
                "emotions": ["Elegant", "Captured", "Artisanal"],
                "colorPalette": ["#2D3436", "#636E72", "#B2BEC3", "#DFE6E9", "#FFFFFF"]
            }

        # STEP 2: Create collage using the engine
        print(f"LOG: Starting Collage Creation for {len(photo_bytes_list)} photos...")
        collage_bytes = create_collage_from_analysis(photo_bytes_list, gemini_json)
        
        # STEP 3: Encode collage to base64
        collage_base64 = base64.b64encode(collage_bytes).decode()

        print("--- REQUEST COMPLETE: COLLAGE GENERATED ---")

        return {
            "analysis": gemini_json,
            "collage_image": f"data:image/png;base64,{collage_base64}",
            "error": None
        }

    except Exception as e:
        print(f"❌ CRITICAL BACKEND ERROR: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "analysis": {
                "dominantEmotion": "Processing...",
                "vibeDescription": "Studio is having a creative block",
                "collageStyle": "moodboard",
                "emotions": ["Patience", "Retry", "Studio"],
                "colorPalette": ["#CCCCCC", "#AAAAAA", "#888888", "#666666", "#444444"]
            },
            "collage_image": None,
            "error": str(e)
        }
