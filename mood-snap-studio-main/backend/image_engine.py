import cv2
import numpy as np
import io
import random
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageChops
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
    ULTRA-HD Watercolor: Optimized for quality with intelligent scaling
    - Uses larger preview size for better quality
    - LANCZOS upscaling to preserve details
    - Enhanced parameters for artistic look
    """
    try:
        orig_size = img.size

        # Step 1: Scale down smartly (larger than before for better quality)
        # Use 1200px instead of 600px for better detail preservation
        scale_width = 1200
        img_small = img.resize((scale_width, int(scale_width * orig_size[1] / orig_size[0])), Image.Resampling.LANCZOS)

        # Step 2: Enhanced Stylization
        img_cv = cv2.cvtColor(np.array(img_small.convert("RGB")), cv2.COLOR_RGB2BGR)
        # Enhanced parameters for more pronounced watercolor effect
        dst = cv2.stylization(img_cv, sigma_s=60, sigma_r=0.45)

        # Step 3: High-quality upscaling back to original size
        img_pil = Image.fromarray(cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))
        img_pil = img_pil.resize(orig_size, Image.Resampling.LANCZOS)

        # Step 4: Subtle sharpening to restore edge definition
        img_pil = ImageEnhance.Sharpness(img_pil).enhance(1.15)

        return img_pil
    except Exception as e:
        print(f"WARNING: Watercolor optimization fallback: {e}")
        return img


def add_doodle_outline(img: Image.Image, width: int = 20, color: str = "#FFFFFF") -> Image.Image:
    """
    Add a thick, slightly jittery white outline to an RGBA cutout.
    """
    if img.mode != 'RGBA':
        return img
    
    # 1. Create a mask from the alpha channel
    alpha = img.split()[3]
    
    # 2. Expand the alpha to create the stroke area
    # MaxFilter is good for creating a clean expansion
    stroke_mask = alpha.filter(ImageFilter.MaxFilter(width * 2 + 1))
    
    # 3. Create the outline image
    r, g, b = hex_to_rgb(color)
    outline = Image.new("RGBA", img.size, (r, g, b, 255))
    
    # 4. Paste the original image over the outline using the expanded mask
    # We use the expanded mask to place the 'outline' color on a new canvas
    canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))
    canvas.paste(outline, (0, 0), mask=stroke_mask)
    
    # 5. Composite the original image ON TOP of the outline
    final = Image.alpha_composite(canvas, img)
    
    # Optional: Slightly blur the outline mask for a softer "sticker" look
    # final = final.filter(ImageFilter.GaussianBlur(radius=1))
    
    return final


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


def apply_super_resolution(img_cv: np.ndarray, max_dimension: int = 4000) -> np.ndarray:
    """
    ULTRA-HD Enhancement: Uses OpenCV detail enhancement for crisp output
    - Sharpens edges using unsharp masking
    - Enhances micro-details
    - Optimized for high-res collage output
    """
    try:
        h, w = img_cv.shape[:2]

        # Only apply if image is below target resolution
        if max(h, w) < max_dimension * 0.7:
            print(f"LOG: Applying super-resolution enhancement (size: {w}x{h})")

            # Method 1: Detail Enhancement using edge-preserving filter
            img_cv = cv2.detailEnhance(img_cv, sigma_s=10, sigma_r=0.15)

            # Method 2: Unsharp masking for crisp details
            gaussian = cv2.GaussianBlur(img_cv, (0, 0), 2.0)
            img_cv = cv2.addWeighted(img_cv, 1.5, gaussian, -0.5, 0)

        return img_cv

    except Exception as e:
        print(f"Super-resolution warning: {e}")
        return img_cv


def apply_luxury_grade(image_bytes: bytes, enable_super_res: bool = True) -> Image.Image:
    """
    ULTRA-HD STUDIO ENHANCER: Professional photo enhancement pipeline
    - Super-resolution for low-res inputs (optional)
    - Bilateral Filtering for skin smoothing
    - CLAHE for adaptive brightness and detail
    - Multi-stage sharpening for crisp output
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img_cv is None: raise ValueError("Decode Error")

        # 0. Super-Resolution Enhancement (for low-res images)
        if enable_super_res:
            img_cv = apply_super_resolution(img_cv)

        # 1. Bilateral Filter: Smooths skin while keeping edges sharp (Luxury Effect)
        img_cv = cv2.bilateralFilter(img_cv, 9, 75, 75)

        # 2. ENHANCED CLAHE: Adaptive Histogram Equalization for 'Pop'
        lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        # Increased clipLimit for more dramatic enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        img_cv = cv2.merge((l, a, b))
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_LAB2BGR)

        # Convert to PIL
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

        # 3. Multi-Stage Sharpening for ULTRA-HD output
        enhancer = ImageEnhance.Sharpness(img_pil)
        img_pil = enhancer.enhance(1.6)  # Increased from 1.4

        # 4. Micro-contrast boost
        enhancer = ImageEnhance.Contrast(img_pil)
        img_pil = enhancer.enhance(1.08)

        return img_pil

    except Exception as e:
        print(f"Enhancement Warning: {e}")
        return Image.open(io.BytesIO(image_bytes))


def apply_filter(img: Image.Image, filter_type: str) -> Image.Image:
    """
    ULTRA-HD Filter System: Preserves quality during artistic processing
    - All filters maintain sharpness and detail
    - No destructive compression
    - Optimized for high-resolution output
    """
    # Convert to RGB if needed (preserve quality)
    if img.mode == 'RGBA':
        # Preserve alpha channel
        alpha = img.split()[3]
        rgb_img = img.convert("RGB")
    else:
        rgb_img = img.convert("RGB")
        alpha = None

    if filter_type == "vintage":
        # High-quality sepia tone
        sepia_matrix = (0.393, 0.769, 0.189, 0, 0.349, 0.686, 0.168, 0, 0.272, 0.534, 0.131, 0)
        rgb_img = rgb_img.convert("RGB", sepia_matrix)
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(0.95)  # Slightly increased
        # Add slight grain for authentic film look
        rgb_img = ImageEnhance.Sharpness(rgb_img).enhance(1.1)

    elif filter_type == "bw":
        # High-quality B&W conversion with detail preservation
        rgb_img = rgb_img.convert("L")
        # Enhanced contrast for dramatic B&W
        rgb_img = ImageEnhance.Contrast(rgb_img.convert("RGB")).enhance(1.3)
        # Slight sharpening to maintain crispness
        rgb_img = ImageEnhance.Sharpness(rgb_img).enhance(1.15)

    elif filter_type == "vibrant":
        # Vibrant colors with quality preservation
        rgb_img = ImageEnhance.Color(rgb_img).enhance(1.5)  # Increased saturation
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.12)  # More contrast
        # Sharpen to prevent color bleeding softness
        rgb_img = ImageEnhance.Sharpness(rgb_img).enhance(1.1)

    elif filter_type == "soft":
        # Soft filter with minimal quality loss
        # Use smaller blur radius to preserve detail
        rgb_img = rgb_img.filter(ImageFilter.GaussianBlur(radius=0.8))
        rgb_img = ImageEnhance.Brightness(rgb_img).enhance(1.12)
        # Light sharpening to counter blur
        rgb_img = ImageEnhance.Sharpness(rgb_img).enhance(1.05)

    elif filter_type == "luxury":
        # Additional luxury enhancements
        rgb_img = ImageEnhance.Contrast(rgb_img).enhance(1.08)
        rgb_img = ImageEnhance.Sharpness(rgb_img).enhance(1.15)

    # Restore alpha channel if it existed
    if alpha is not None:
        rgb_img.putalpha(alpha)

    return rgb_img


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
    ULTRA-HD Resize: Smart upscaling with quality preservation
    - If image is smaller than target, upscales first with sharpening
    - Uses LANCZOS for maximum sharpness
    - Preserves detail during scaling
    """
    original_width, original_height = img.size
    ratio = min(max_width / original_width, max_height / original_height)
    new_size = (int(original_width * ratio), int(original_height * ratio))

    # Smart Upscaling: If we're scaling UP (ratio > 1), apply pre-sharpening
    if ratio > 1.0:
        print(f"LOG: Smart upscaling from {img.size} to {new_size} (ratio: {ratio:.2f})")
        # Pre-sharpen before upscaling to preserve detail
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.6)

        # Use LANCZOS for upscaling
        resized = img.resize(new_size, Image.Resampling.LANCZOS)

        # Post-upscale enhancement to restore crispness
        resized = ImageEnhance.Sharpness(resized).enhance(1.3)
        resized = ImageEnhance.Contrast(resized).enhance(1.05)

        return resized
    else:
        # Downscaling: Use LANCZOS directly (already optimal)
        return img.resize(new_size, Image.Resampling.LANCZOS)


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
