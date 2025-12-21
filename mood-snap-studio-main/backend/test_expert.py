import sys
sys.path.insert(0, '.')

from collage_engine import CollageEngine
from PIL import Image
import io
import time

# Create a simple test
engine = CollageEngine()

# Create dummy photo bytes
print("Generating test images...")
test_photos = []
for i in range(2): # Test with 2 photos
    img = Image.new('RGB', (800, 800), color=(100 + 50*i, 150, 200))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    test_photos.append(buf.getvalue())

# Test Scrapbook (uses rembg)
test_analysis = {
    "collageStyle": "scrapbook",
    "colorPalette": ["#FF6B6B", "#4ECDC4", "#FFEEAD"],
    "dominantEmotion": "Joy"
}

print("Running Expert Collage Engine (this might take a few seconds for rembg)...")
start_time = time.time()
try:
    result = engine.create_collage(test_photos, "scrapbook", test_analysis["colorPalette"], test_analysis["dominantEmotion"])
    end_time = time.time()
    print(f"SUCCESS! Created AI-powered collage in {end_time - start_time:.2f} seconds")
    print(f"Result size: {len(result)} bytes")
    
    with open("test_expert_collage.jpg", "wb") as f:
        f.write(result)
    print("Saved to test_expert_collage.jpg")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
