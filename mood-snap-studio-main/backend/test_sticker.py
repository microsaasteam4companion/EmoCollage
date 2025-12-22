import sys
import os
sys.path.insert(0, '.')

from collage_engine import CollageEngine
from PIL import Image
import io
import time

# Create a simple test
engine = CollageEngine()

# Use the uploaded image for testing
image_path = r"C:\Users\LENOVO\.gemini\antigravity\brain\baa72bbf-0bf3-4487-a063-b0e01f0fa592\uploaded_image_1766394800655.jpg"

if not os.path.exists(image_path):
    print(f"Error: Could not find test image at {image_path}")
    # Create dummy photo bytes if file not found
    test_photos = []
    for i in range(3):
        img = Image.new('RGB', (800, 1200), color=(100 + 50*i, 150, 200))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        test_photos.append(buf.getvalue())
else:
    print(f"Loading test image from {image_path}...")
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    test_photos = [img_bytes] * 5 # Use the same image multiple times for the layout

test_analysis = {
    "collageStyle": "sticker",
    "colorPalette": ["#BDC3C7", "#F1C40F", "#FF6B6B"],
    "dominantEmotion": "Fun"
}

print("Running Sticker Collage Engine (Background removal may take a moment)...")
start_time = time.time()
try:
    result = engine.create_collage(
        test_photos, 
        test_analysis["collageStyle"], 
        test_analysis["colorPalette"], 
        test_analysis["dominantEmotion"]
    )
    end_time = time.time()
    print(f"SUCCESS! Created Sticker collage in {end_time - start_time:.2f} seconds")
    
    # Save as PNG since the engine exports PNG to preserve quality/alpha internally
    output_path = "test_sticker_collage.png"
    with open(output_path, "wb") as f:
        f.write(result)
    print(f"Saved to {output_path}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
