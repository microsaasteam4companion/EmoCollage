import cv2
import numpy as np
import io
import random
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
from typing import Tuple, Optional
from rembg import remove


def create_cutout(img_bytes: bytes) -> Image.Image:
    """
    Remove background to create a professional cutout/sticker.
    SAFE VERSION: If it fails or is slow, it returns the original with luxury grading.
    """
    try:
        print("LOG: Attempting Background Removal (this may take a moment)...")
        # Use rembg with a quick check
        output = remove(img_bytes)
        return Image.open(io.BytesIO(output)).convert("RGBA")
    except Exception as e:
        print(f"WARNING: Background removal skipped/failed: {e}")
        # Fallback: Just used the luxury graded image
        img = apply_luxury_grade(img_bytes)
        return img.convert("RGBA")


def apply_watercolor_effect(img: Image.Image) -> Image.Image:
    """
    Studio Optimized: Downscales before stylizing to save minutes of CPU time.
    """
    try:
        orig_size = img.size
        # Step 1: Scale down for speed (OpenCV stylization is extremely heavy)
        img_small = img.resize((600, int(600 * orig_size[1] / orig_size[0])), Image.Resampling.BILINEAR)
        
        # Step 2: Stylize
        img_cv = cv2.cvtColor(np.array(img_small.convert("RGB")), cv2.COLOR_RGB2BGR)
        dst = cv2.stylization(img_cv, sigma_s=30, sigma_r=0.3)
        
        # Step 3: Scale back up
        img_pil = Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
        return img_pil.resize(orig_size, Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"WARNING: Watercolor optimization fallback: {e}")
        return img


def add_premium_shadow(img: Image.Image, offset: Tuple[int, int] = (20, 20), 
                       blur_radius: int = 40) -> Image.Image:
    """
    Studio-Grade Shadow: Deep, soft, and realistic.
    """
    # Expanded canvas for the soft blur spread
    pad = blur_radius * 2
    bg_width = img.width + pad * 2
    bg_height = img.height + pad * 2
    
    # 1. Create Shadow Alpha
    shadow = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
    # Extract original alpha or create full white mask
    if img.mode == 'RGBA':
        alpha = img.split()[3]
    else:
        alpha = Image.new("L", img.size, 255)
    
    # 2. Draw Shadow Layer (Deep but transparent)
    shadow_color = Image.new("RGBA", img.size, (0, 0, 0, 65)) # Soft 65 alpha
    shadow.paste(shadow_color, (pad + offset[0], pad + offset[1]), mask=alpha)
    
    # 3. Apply Multi-Stage Gaussian Blur for 'Studio' softness
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # 4. Paste Image Over Shadow
    final = Image.new("RGBA", (bg_width, bg_height), (0, 0, 0, 0))
    final.paste(img.convert("RGBA"), (pad, pad), mask=alpha)
    
    return Image.alpha_composite(shadow, final)


def add_washi_tape(canvas: Image.Image, x: int, y: int, angle: float, color: str):
    """
    Add a realistic semi-transparent washi tape with torn edges.
    """
    tape_width = 120
    tape_height = 40
    
    # Create tape image
    tape = Image.new("RGBA", (tape_width, tape_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tape)
    
    # Main tape body with transparency
    r, g, b = hex_to_rgb(color)
    draw.rectangle([5, 0, tape_width-5, tape_height], fill=(r, g, b, 160))
    
    # Torn edges effect
    for i in range(0, tape_height, 4):
        draw.chord([0, i, 10, i+4], 90, 270, fill=(0, 0, 0, 0))
        draw.chord([tape_width-10, i, tape_width, i+4], 270, 90, fill=(0, 0, 0, 0))
        
    # Rotate and paste
    rotated_tape = tape.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    canvas.paste(rotated_tape, (x, y), rotated_tape)


def add_hand_drawn_doodle(canvas: Image.Image, doodle_type: str, x: int, y: int, size: int, color: str):
    """
    Draw a doodle that looks hand-drawn (jittery lines, varying thickness).
    """
    doodle_canvas = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(doodle_canvas)
    r, g, b = hex_to_rgb(color)
    full_color = (r, g, b, 200)
    
    def jitter_point(p, j=2):
        return (p[0] + random.randint(-j, j), p[1] + random.randint(-j, j))
    
    cx, cy = size, size
    
    if doodle_type == "heart":
        # Draw heart with multiple strokes for hand-drawn look
        for _ in range(2):
            points = []
            for t in range(0, 32):
                angle = (t / 31) * 2 * 3.14159
                # Heart formula
                hx = 16 * (np.sin(angle)**3)
                hy = -(13 * np.cos(angle) - 5 * np.cos(2*angle) - 2 * np.cos(3*angle) - np.cos(4*angle))
                points.append(jitter_point((cx + hx * size/25, cy + hy * size/25)))
            draw.line(points, fill=full_color, width=random.randint(2, 4), joint="round")

    elif doodle_type == "star":
        for _ in range(2):
            points = []
            for i in range(11):
                angle = (i * 3.14159 * 2 / 5) - (3.14159 / 2)
                radius = size * 0.8 if i % 2 == 0 else size * 0.4
                px = cx + np.cos(angle) * radius
                py = cy + np.sin(angle) * radius
                points.append(jitter_point((px, py)))
            draw.line(points, fill=full_color, width=random.randint(2, 4), joint="round")
            
    elif doodle_type == "squiggle":
        points = []
        for i in range(10):
            px = cx - size + (i * size * 2 / 9)
            py = cy + np.sin(i * 1.5) * (size/3)
            points.append(jitter_point((px, py), 4))
        draw.line(points, fill=full_color, width=4, joint="round")

    # Paste onto main canvas
    canvas.paste(doodle_canvas, (x - size, y - size), doodle_canvas)


def apply_luxury_grade(image_bytes: bytes) -> Image.Image:
    """
    PERMANENT SOLUTION: Studio Photo Enhancer
    Uses Bilateral Filtering for skin smoothing and CLAHE for crisp details.
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img_cv is None: raise ValueError("Decode Error")
            
        # 1. Bilateral Filter: Smooths skin while keeping edges sharp (Luxury Effect)
        img_cv = cv2.bilateralFilter(img_cv, 9, 75, 75)
        
        # 2. CLAHE: Adaptive Histogram Equalization for 'Pop'
        lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l = clahe.apply(l)
        img_cv = cv2.merge((l, a, b))
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_LAB2BGR)
        
        # Convert to PIL
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        
        # 3. Final Sharpening
        enhancer = ImageEnhance.Sharpness(img_pil)
        return enhancer.enhance(1.4)
        
    except Exception as e:
        print(f"Enhancement Warning: {e}")
        return Image.open(io.BytesIO(image_bytes))


def apply_filter(img: Image.Image, filter_type: str) -> Image.Image:
    if filter_type == "vintage":
        img = img.convert("RGB")
        sepia_matrix = (0.393, 0.769, 0.189, 0, 0.349, 0.686, 0.168, 0, 0.272, 0.534, 0.131, 0)
        img = img.convert("RGB", sepia_matrix)
        img = ImageEnhance.Contrast(img).enhance(0.9)
    elif filter_type == "bw":
        img = img.convert("L").convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(1.2)
    elif filter_type == "vibrant":
        img = ImageEnhance.Color(img).enhance(1.4)
        img = ImageEnhance.Contrast(img).enhance(1.1)
    elif filter_type == "soft":
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        img = ImageEnhance.Brightness(img).enhance(1.1)
    elif filter_type == "luxury":
        # Handled by separate function but kept for mapping
        pass
    return img


def add_polaroid_frame(img: Image.Image, border_color: str = "white") -> Image.Image:
    width, height = img.size
    border_width = int(width * 0.05)
    bottom_border = int(height * 0.15)
    new_width = width + (border_width * 2)
    new_height = height + border_width + bottom_border
    framed = Image.new("RGB", (new_width, new_height), border_color)
    framed.paste(img, (border_width, border_width))
    return framed


def add_studio_texture(img: Image.Image) -> Image.Image:
    """
    Optimized physical texture generation.
    """
    try:
        width, height = img.size
        # Uniform noise is much faster to generate than Normal distribution
        noise = np.random.randint(-15, 15, (height, width), dtype=np.int16)
        noise_stack = np.stack([noise]*3, axis=-1)
        # Shift to mid-gray and blend
        noise_img = Image.fromarray(np.uint8(np.clip(noise_stack + 128, 0, 255)), mode='RGB')
        
        return Image.blend(img.convert("RGB"), noise_img.convert("RGB"), alpha=0.04)
    except Exception as e:
        print(f"Texture error: {e}")
        return img


def rotate_image(img: Image.Image, angle: float = None) -> Image.Image:
    if angle is None: angle = random.uniform(-8, 8)
    return img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)


def create_gradient_background(width: int, height: int, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> Image.Image:
    base = Image.new("RGB", (width, height), color1)
    top = Image.new("RGB", (width, height), color2)
    mask = Image.new("L", (width, height))
    mask.putdata([int(255 * (y / height)) for y in range(height) for _ in range(width)])
    base.paste(top, (0, 0), mask)
    return base


def resize_to_fit(img: Image.Image, max_width: int, max_height: int) -> Image.Image:
    """
    HD Resize: Uses LANCZOS for maximum sharpness.
    """
    # Calculate aspect ratio
    ratio = min(max_width / img.width, max_height / img.height)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    
    # Use LANCZOS (Highest quality)
    return img.resize(new_size, Image.Resampling.LANCZOS)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
