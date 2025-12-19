"""
Enhanced Image Processing Engine for Collage Creation
Provides filters, effects, blending, and composition utilities
"""

import cv2
import numpy as np
import io
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
from typing import Tuple, Optional
import random


def apply_luxury_grade(image_bytes: bytes) -> Image.Image:
    """
    Applies 'Luxury Studio' grading using Computer Vision techniques.
    1. Smart Sharpening (Unsharp Mask)
    2. Adaptive Contrast (CLAHE)
    3. Cinematic Color Grading
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # LAB color space processing
        lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # CLAHE for detail enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        
        limg = cv2.merge((cl, a, b))
        final_lab = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        img_pil = Image.fromarray(cv2.cvtColor(final_lab, cv2.COLOR_BGR2RGB))
        
        # Polish
        enhancer_sharp = ImageEnhance.Sharpness(img_pil)
        img_pil = enhancer_sharp.enhance(1.2)
        
        enhancer_col = ImageEnhance.Color(img_pil)
        img_pil = enhancer_col.enhance(1.05)
        
        return img_pil
        
    except Exception as e:
        print(f"Error in luxury grading: {e}")
        return Image.open(io.BytesIO(image_bytes))


def apply_filter(img: Image.Image, filter_type: str) -> Image.Image:
    """
    Apply Instagram-style filters
    Options: vintage, bw, vibrant, soft, warm, cool
    """
    if filter_type == "vintage":
        # Sepia tone + vignette
        img = img.convert("RGB")
        sepia_matrix = (
            0.393, 0.769, 0.189, 0,
            0.349, 0.686, 0.168, 0,
            0.272, 0.534, 0.131, 0
        )
        img = img.convert("RGB", sepia_matrix)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(0.9)
        
    elif filter_type == "bw":
        img = img.convert("L").convert("RGB")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
    elif filter_type == "vibrant":
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.4)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
    elif filter_type == "soft":
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)
        
    elif filter_type == "warm":
        # Add warm tint
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        # Tint overlay would go here
        
    elif filter_type == "cool":
        # Add cool tint
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.9)
    
    return img


def add_polaroid_frame(img: Image.Image, border_color: str = "white") -> Image.Image:
    """
    Add realistic polaroid-style frame with shadow
    """
    # Calculate frame dimensions
    width, height = img.size
    border_width = int(width * 0.05)  # 5% border
    bottom_border = int(height * 0.15)  # 15% bottom for that polaroid look
    
    # Create new image with borders
    new_width = width + (border_width * 2)
    new_height = height + border_width + bottom_border
    
    framed = Image.new("RGB", (new_width, new_height), border_color)
    framed.paste(img, (border_width, border_width))
    
    return framed


def add_shadow(img: Image.Image, offset: Tuple[int, int] = (10, 10), 
               blur_radius: int = 15, shadow_color: str = "black") -> Image.Image:
    """
    Add drop shadow effect to image
    """
    # Create shadow layer
    shadow = Image.new("RGBA", 
                      (img.width + offset[0] * 2, img.height + offset[1] * 2), 
                      (0, 0, 0, 0))
    
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle(
        [offset[0], offset[1], img.width + offset[0], img.height + offset[1]],
        fill=(0, 0, 0, 100)
    )
    
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Composite
    result = Image.new("RGBA", shadow.size, (255, 255, 255, 0))
    result.paste(shadow, (0, 0))
    result.paste(img.convert("RGBA"), offset)
    
    return result


def add_texture(img: Image.Image, texture_type: str = "paper") -> Image.Image:
    """
    Add subtle texture overlay (paper, grain, canvas)
    """
    # Create noise texture
    width, height = img.size
    noise = np.random.randint(0, 50, (height, width), dtype=np.uint8)
    noise_img = Image.fromarray(noise, mode='L').convert("RGB")
    
    # Blend with original
    result = Image.blend(img.convert("RGB"), noise_img, alpha=0.05)
    return result


def rotate_image(img: Image.Image, angle: float = None) -> Image.Image:
    """
    Rotate image with random angle if not specified
    """
    if angle is None:
        angle = random.uniform(-8, 8)
    
    return img.rotate(angle, expand=True, fillcolor="white")


def create_gradient_background(width: int, height: int, 
                               color1: Tuple[int, int, int],
                               color2: Tuple[int, int, int]) -> Image.Image:
    """
    Create a gradient background
    """
    base = Image.new("RGB", (width, height), color1)
    top = Image.new("RGB", (width, height), color2)
    
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    
    base.paste(top, (0, 0), mask)
    return base


def resize_to_fit(img: Image.Image, max_width: int, max_height: int) -> Image.Image:
    """
    Resize image to fit within bounds while maintaining aspect ratio
    """
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    return img


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
