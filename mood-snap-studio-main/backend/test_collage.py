import sys
sys.path.insert(0, '.')

from collage_engine import CollageEngine
from PIL import Image
import io

# Create a simple test
engine = CollageEngine()

# Create dummy photo bytes (small test images)
test_photos = []
for i in range(3):
    img = Image.new('RGB', (400, 400), color=(255, 100*i, 100*i))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    test_photos.append(buf.getvalue())

# Test analysis
test_analysis = {
    "collageStyle": "scrapbook",
    "colorPalette": ["#FF6B6B", "#4ECDC4", "#FFEEAD"],
    "dominantEmotion": "Joy"
}

try:
    result = engine.create_collage(test_photos, "scrapbook", test_analysis["colorPalette"], test_analysis["dominantEmotion"])
    print(f"SUCCESS! Created collage of {len(result)} bytes")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
