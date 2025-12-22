"""
Main Collage Composition Engine
Orchestrates template selection, image processing, and final composition
"""

import io
import random
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
import base64

from collage_templates import get_template_by_style, CollageTemplate, PhotoPlacement
from image_engine import (
    apply_luxury_grade, apply_filter, add_polaroid_frame,
    add_premium_shadow, add_studio_texture, rotate_image, create_gradient_background,
    resize_to_fit, hex_to_rgb, create_cutout, apply_watercolor_effect,
    add_washi_tape, add_hand_drawn_doodle, add_doodle_outline
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
        """
        num_photos = len(photo_bytes_list)
        
        # 1. Select appropriate template
        self.template = get_template_by_style(style, num_photos)
        
        # 2. Create canvas with background
        self.canvas = self._create_background()
        self.canvas = self.canvas.convert("RGBA")
        
        # 3. Process each photo first (collect in a list for sorting)
        layers = []
        total_photos = len(photo_bytes_list)
        available_slots = len(self.template.placements)
        
        print(f"LOG: Engine received {total_photos} photos. Selected template '{self.template.name}' has {available_slots} slots.")
        
        for i, photo_bytes in enumerate(photo_bytes_list):
            if i >= available_slots:
                print(f"LOG: Skipping photo {i+1} (No more slots in template)")
                break
            
            print(f"LOG: Processing Photo {i+1}/{total_photos}...")
            placement = self.template.placements[i]
            try:
                processed_photo = self._process_photo(photo_bytes, placement)
                layers.append((processed_photo, placement))
                print(f"LOG: Photo {i+1} layer created successfully.")
            except Exception as e:
                print(f"ERROR: Failed photo {i+1} processing: {e}")
        
        # 4. Sort layers by z_index
        print(f"LOG: Sorting {len(layers)} layers for composition...")
        layers.sort(key=lambda x: getattr(x[1], 'z_index', 0))
        
        # 5. Place sorted layers
        for idx, (photo, placement) in enumerate(layers):
            print(f"LOG: Pasting layer {idx+1}/{len(layers)} onto canvas...")
            self._place_photo(photo, placement)
        
        # 6. Add decorative elements (stickers, doodles)
        self._add_decorations(color_palette, emotion)
        
        # 7. Final Studio Polish (HD Texture)
        print("LOG: Applying final Studio Polish (Paper/Film Texture)...")
        self.canvas = add_studio_texture(self.canvas)

        # 8. ULTRA-HD Export with maximum quality
        print("LOG: Exporting ULTRA-HD collage (PNG with maximum quality)...")
        output = io.BytesIO()

        # Convert to RGB for final export if needed (preserves quality)
        if self.canvas.mode == 'RGBA':
            # Create white background for transparency
            background = Image.new('RGB', self.canvas.size, (255, 255, 255))
            background.paste(self.canvas, mask=self.canvas.split()[3] if self.canvas.mode == 'RGBA' else None)
            export_canvas = background
        else:
            export_canvas = self.canvas.convert('RGB')

        # Maximum quality PNG export
        # compress_level=1 (fast but larger file, better quality than optimize=True)
        export_canvas.save(output, format='PNG', compress_level=1)

        print(f"LOG: Final collage size: {export_canvas.size}, Mode: {export_canvas.mode}")
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
            color = hex_to_rgb(self.template.background_colors[0])
            return Image.new("RGB", (width, height), color)
    
    def _process_photo(self, photo_bytes: bytes, placement: PhotoPlacement) -> Image.Image:
        """Process a single photo with expert effects"""
        # 1. Background removal optimization (only if template suggests it)
        if getattr(placement, "use_cutout", False):
            img = create_cutout(photo_bytes)
        else:
            img = apply_luxury_grade(photo_bytes)
            
        # 2. Resize
        img = resize_to_fit(img, placement.width, placement.height)
        
        # 3. Artistic filters
        if placement.filter == "watercolor":
            img = apply_watercolor_effect(img)
        elif placement.filter != "none":
            img = apply_filter(img, placement.filter)
        
        # 4. Frames
        if placement.frame_style == "polaroid":
            img = add_polaroid_frame(img, "white")
        
        # 5. Rotation
        if placement.rotation != 0:
            img = rotate_image(img, placement.rotation)
            
        # 6. Doodle Outlines (New Feature)
        if getattr(placement, "use_outline", False):
            print(f"LOG: Applying doodle outline (width: {placement.outline_width})...")
            # For quality, we apply outline after resizing but before shadow
            img = add_doodle_outline(img, placement.outline_width, placement.outline_color)

        # 7. Premium Shadow
        if not getattr(placement, "no_shadow", False):
            img = add_premium_shadow(img)
        
        return img
    
    def _place_photo(self, photo: Image.Image, placement: PhotoPlacement):
        """Place processed photo on canvas using alpha composition"""
        final_x = placement.x
        final_y = placement.y
        
        print(f"LOG: Composing photo at ({final_x}, {final_y})...")
        
        # Expert Fix: Ensure RGBA for transparency support
        if photo.mode != 'RGBA':
            photo = photo.convert('RGBA')
            
        # Create temp layer
        layer = Image.new("RGBA", self.canvas.size, (0, 0, 0, 0))
        layer.paste(photo, (final_x, final_y), photo)
        
        # Merge with main canvas
        self.canvas = Image.alpha_composite(self.canvas, layer)
    
    def _add_decorations(self, color_palette: List[str], emotion: str):
        """Add expert decorations"""
        for decoration in self.template.decorations:
            dec_type = decoration.get("type")
            color = color_palette[0] if color_palette else "#000000"
            
            if dec_type == "doodle":
                add_hand_drawn_doodle(
                    self.canvas, 
                    decoration.get("shape", "heart"),
                    decoration["x"], 
                    decoration["y"], 
                    decoration.get("size", 60),
                    decoration.get("color", color)
                )
            elif dec_type == "washi_tape":
                add_washi_tape(
                    self.canvas,
                    decoration["x"],
                    decoration["y"],
                    decoration.get("rotation", 0),
                    decoration.get("color", color)
                )
            elif dec_type == "text":
                self._draw_text(decoration)
    
    def _draw_text(self, decoration: dict):
        """Draw high-quality text"""
        draw = ImageDraw.Draw(self.canvas)
        try:
            # We try for a serif or handwritten font if available
            font = ImageFont.truetype("arialbi.ttf", decoration.get("font_size", 40))
        except:
            font = ImageFont.load_default()
        
        # Add slight shadow to text
        draw.text(
            (decoration["x"]+2, decoration["y"]+2),
            decoration["content"],
            fill=(0, 0, 0, 100),
            font=font
        )
        draw.text(
            (decoration["x"], decoration["y"]),
            decoration["content"],
            fill=decoration.get("color", "#000000"),
            font=font
        )


def create_collage_from_analysis(photos: List[bytes], analysis: dict) -> bytes:
    engine = CollageEngine()
    style = analysis.get("collageStyle", "moodboard")
    palette = analysis.get("colorPalette", ["#FFFFFF", "#000000"])
    emotion = analysis.get("dominantEmotion", "Joy")
    return engine.create_collage(photos, style, palette, emotion)
