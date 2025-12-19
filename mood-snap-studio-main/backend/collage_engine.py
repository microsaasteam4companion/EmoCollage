"""
Main Collage Composition Engine
Orchestrates template selection, image processing, and final composition
"""

import io
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
import base64

from collage_templates import get_template_by_style, CollageTemplate, PhotoPlacement
from image_engine import (
    apply_luxury_grade, apply_filter, add_polaroid_frame,
    add_shadow, add_texture, rotate_image, create_gradient_background,
    resize_to_fit, hex_to_rgb
)


class CollageEngine:
    """Main engine for creating professional collages"""
    
    def __init__(self):
        self.canvas = None
        self.template = None
        
    def create_collage(self, 
                      photo_bytes_list: List[bytes],
                      style: str,
                      color_palette: List[str],
                      emotion: str) -> bytes:
        """
        Main method to create a complete collage
        
        Args:
            photo_bytes_list: List of image bytes
            style: Detected style (e.g., "magazine", "scrapbook")
            color_palette: AI-detected color palette
            emotion: Dominant emotion
            
        Returns:
            bytes: Final composed collage as PNG bytes
        """
        num_photos = len(photo_bytes_list)
        
        # 1. Select appropriate template
        self.template = get_template_by_style(style, num_photos)
        
        # 2. Create canvas with background
        self.canvas = self._create_background()
        
        # 3. Process and place each photo
        for i, photo_bytes in enumerate(photo_bytes_list):
            if i >= len(self.template.placements):
                break  # Don't exceed template capacity
                
            placement = self.template.placements[i]
            processed_photo = self._process_photo(photo_bytes, placement)
            self._place_photo(processed_photo, placement)
        
        # 4. Add decorative elements
        self._add_decorations(color_palette, emotion)
        
        # 5. Final polish
        self.canvas = add_texture(self.canvas, "paper")
        
        # 6. Convert to bytes
        output = io.BytesIO()
        self.canvas.save(output, format='PNG', quality=95)
        output.seek(0)
        
        return output.getvalue()
    
    def _create_background(self) -> Image.Image:
        """Create the canvas background"""
        width = self.template.canvas_width
        height = self.template.canvas_height
        
        if self.template.background_type == "gradient":
            color1 = hex_to_rgb(self.template.background_colors[0])
            color2 = hex_to_rgb(self.template.background_colors[1] if len(self.template.background_colors) > 1 else self.template.background_colors[0])
            return create_gradient_background(width, height, color1, color2)
        else:
            # Solid color
            color = hex_to_rgb(self.template.background_colors[0])
            return Image.new("RGB", (width, height), color)
    
    def _process_photo(self, photo_bytes: bytes, placement: PhotoPlacement) -> Image.Image:
        """Process a single photo according to placement specs"""
        # 1. Load and apply luxury grading
        img = apply_luxury_grade(photo_bytes)
        
        # 2. Resize to fit placement
        img = resize_to_fit(img, placement.width, placement.height)
        
        # 3. Apply filter if specified
        if placement.filter != "none":
            img = apply_filter(img, placement.filter)
        
        # 4. Add frame if specified
        if placement.frame_style == "polaroid":
            img = add_polaroid_frame(img, "white")
        elif placement.frame_style == "border":
            img = self._add_simple_border(img, 10, "white")
        
        # 5. Rotate if needed
        if placement.rotation != 0:
            img = rotate_image(img, placement.rotation)
        
        return img
    
    def _add_simple_border(self, img: Image.Image, border_width: int, color: str) -> Image.Image:
        """Add simple border around image"""
        new_width = img.width + (border_width * 2)
        new_height = img.height + (border_width * 2)
        
        bordered = Image.new("RGB", (new_width, new_height), color)
        bordered.paste(img, (border_width, border_width))
        
        return bordered
    
    def _place_photo(self, photo: Image.Image, placement: PhotoPlacement):
        """Place processed photo on canvas"""
        # For rotated images, we need to handle positioning carefully
        self.canvas.paste(photo, (placement.x, placement.y), photo if photo.mode == 'RGBA' else None)
    
    def _add_decorations(self, color_palette: List[str], emotion: str):
        """Add decorative elements like doodles, text, stickers"""
        draw = ImageDraw.Draw(self.canvas)
        
        for decoration in self.template.decorations:
            dec_type = decoration.get("type")
            
            if dec_type == "doodle":
                self._draw_doodle(draw, decoration, color_palette)
            elif dec_type == "text":
                self._draw_text(draw, decoration)
            elif dec_type == "washi_tape":
                self._draw_washi_tape(draw, decoration)
            elif dec_type == "color_swatch":
                self._draw_color_swatches(draw, decoration, color_palette)
    
    def _draw_doodle(self, draw: ImageDraw.Draw, decoration: dict, palette: List[str]):
        """Draw simple doodle shapes"""
        shape = decoration.get("shape", "circle")
        x, y = decoration["x"], decoration["y"]
        size = decoration.get("size", 50)
        color = decoration.get("color", palette[0] if palette else "#000000")
        
        if shape == "heart":
            # Simple heart approximation
            draw.ellipse([x, y, x+size//2, y+size//2], outline=color, width=3)
            draw.ellipse([x+size//2, y, x+size, y+size//2], outline=color, width=3)
        elif shape == "star":
            # Simple star
            points = self._get_star_points(x, y, size)
            draw.polygon(points, outline=color, width=3)
        elif shape == "circle":
            draw.ellipse([x, y, x+size, y+size], outline=color, width=3)
        elif shape == "squiggle":
            # Random squiggly line
            points = [(x, y), (x+size//3, y-20), (x+2*size//3, y+20), (x+size, y)]
            draw.line(points, fill=color, width=4)
    
    def _get_star_points(self, cx: int, cy: int, size: int) -> List[Tuple[int, int]]:
        """Generate points for a 5-pointed star"""
        import math
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10 - math.pi / 2
            radius = size if i % 2 == 0 else size // 2
            x = cx + int(radius * math.cos(angle))
            y = cy + int(radius * math.sin(angle))
            points.append((x, y))
        return points
    
    def _draw_text(self, draw: ImageDraw.Draw, decoration: dict):
        """Draw text overlay"""
        try:
            # Try to use a nice font, fallback to default
            font = ImageFont.truetype("arial.ttf", decoration.get("font_size", 32))
        except:
            font = ImageFont.load_default()
        
        draw.text(
            (decoration["x"], decoration["y"]),
            decoration["content"],
            fill=decoration.get("color", "#000000"),
            font=font
        )
    
    def _draw_washi_tape(self, draw: ImageDraw.Draw, decoration: dict):
        """Draw washi tape effect"""
        x, y = decoration["x"], decoration["y"]
        color = decoration.get("color", "#FFB6C1")
        
        # Simple rectangle with transparency effect
        draw.rectangle(
            [x, y, x+100, y+30],
            fill=color,
            outline=color
        )
    
    def _draw_color_swatches(self, draw: ImageDraw.Draw, decoration: dict, palette: List[str]):
        """Draw color palette swatches"""
        x, y = decoration["x"], decoration["y"]
        swatch_size = 40
        spacing = 10
        
        for i, color in enumerate(palette[:5]):  # Max 5 swatches
            swatch_x = x
            swatch_y = y + (i * (swatch_size + spacing))
            draw.rectangle(
                [swatch_x, swatch_y, swatch_x+swatch_size, swatch_y+swatch_size],
                fill=color,
                outline="#FFFFFF",
                width=2
            )


def create_collage_from_analysis(photos: List[bytes], analysis: dict) -> bytes:
    """
    Convenience function to create collage from analysis results
    
    Args:
        photos: List of photo bytes
        analysis: Analysis dict with style, colorPalette, dominantEmotion
        
    Returns:
        bytes: PNG collage
    """
    engine = CollageEngine()
    
    style = analysis.get("collageStyle", "moodboard")
    palette = analysis.get("colorPalette", ["#FFFFFF", "#000000"])
    emotion = analysis.get("dominantEmotion", "Joy")
    
    return engine.create_collage(photos, style, palette, emotion)
