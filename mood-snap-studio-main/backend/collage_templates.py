"""
Collage Template Definitions
Pinterest-inspired layouts with precise positioning and styling
"""

from typing import List, Dict, Tuple, Any
from dataclasses import dataclass


@dataclass
class PhotoPlacement:
    """Defines how a photo should be placed in the template"""
    x: int
    y: int
    width: int
    height: int
    rotation: float = 0
    frame_style: str = "none" # none, polaroid, border
    filter: str = "none" # none, luxury, vintage, bw, vibrant, soft, watercolor
    z_index: int = 0
    use_cutout: bool = False # Use background removal
    use_outline: bool = False # Use doodle outline
    outline_width: int = 20
    outline_color: str = "#FFFFFF"
    no_shadow: bool = False


@dataclass
class CollageTemplate:
    """Complete template definition"""
    name: str
    canvas_width: int
    canvas_height: int
    background_type: str  # solid, gradient, texture
    background_colors: List[str]  # Hex colors
    placements: List[PhotoPlacement]
    decorations: List[Dict[str, Any]]  # Stickers, text, etc.


# ============================================================================
# TEMPLATE 1: SCRAPBOOK STYLE
# ============================================================================
def get_scrapbook_template(num_photos: int) -> CollageTemplate:
    """
    Expert Scrapbook: Ultra-HD Studio Layout (3500px)
    """
    canvas_w, canvas_h = 2800, 3800
    placements = [
        # Main photo - Studio Hero
        PhotoPlacement(x=150, y=150, width=2500, height=3000, rotation=0, 
                      frame_style="none", filter="none", z_index=1, use_cutout=True),
        
        # Supporting 1 - Polaroid Top Right
        PhotoPlacement(x=1800, y=250, width=850, height=1100, rotation=4, 
                      frame_style="polaroid", filter="luxury", z_index=5),
        
        # Supporting 2 - Polaroid Bottom Left
        PhotoPlacement(x=150, y=2500, width=800, height=1050, rotation=-6, 
                      frame_style="polaroid", filter="luxury", z_index=4),
        
        # Supporting 3 - Side accent
        PhotoPlacement(x=1950, y=2400, width=700, height=900, rotation=8, 
                      frame_style="polaroid", filter="soft", z_index=3),
    ]
    
    decorations = [
        {"type": "washi_tape", "x": 1900, "y": 200, "rotation": 4, "color": "#DCDDE1"},
        {"type": "text", "content": "COLLECTED MOMENTS", "x": 100, "y": 3600, "font_size": 180, "color": "#2F3640"},
    ]
    
    return CollageTemplate(
        name="Scrapbook",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        background_type="solid",
        background_colors=["#F5F6FA"],
        placements=placements[:num_photos],
        decorations=decorations
    )


# ============================================================================
# TEMPLATE 2: MAGAZINE EDITORIAL
# ============================================================================
def get_magazine_template(num_photos: int) -> CollageTemplate:
    """
    Expert Magazine: Ultra-HD Editorial Spread (3000px)
    """
    canvas_w, canvas_h = 3000, 4000
    placements = [
        # Hero Image (Full Width)
        PhotoPlacement(x=0, y=0, width=3000, height=2200, rotation=0, 
                      frame_style="none", filter="luxury", z_index=1),
        
        # Inset Left
        PhotoPlacement(x=150, y=2300, width=1300, height=1500, rotation=0, 
                      frame_style="border", filter="bw", z_index=5),
        
        # Inset Right
        PhotoPlacement(x=1550, y=2500, width=1300, height=1300, rotation=0, 
                      frame_style="border", filter="vibrant", z_index=4),
    ]
    
    decorations = [
        {"type": "text", "content": "THE NEW ERA", "x": 150, "y": 150, "font_size": 320, "color": "#FFFFFF"},
        {"type": "text", "content": "STUDIO COLLECTION // 2025", "x": 1550, "y": 2320, "font_size": 75, "color": "#2D3436"},
    ]
    
    return CollageTemplate(
        name="Magazine",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        background_type="solid",
        background_colors=["#FFFFFF"],
        placements=placements[:num_photos],
        decorations=decorations
    )


def get_moodboard_template(num_photos: int) -> CollageTemplate:
    """
    Expert Moodboard: Ultra-HD Pinterest-style aesthetic Grid (3000px)
    """
    canvas_w, canvas_h = 3000, 3000 # Perfect Square HD
    placements = [
        # Main Hero (Top Left)
        PhotoPlacement(x=100, y=100, width=1700, height=2200, rotation=0, 
                      frame_style="none", filter="soft", z_index=1),
        
        # Side Column
        PhotoPlacement(x=1900, y=150, width=950, height=1400, rotation=0, 
                      frame_style="none", filter="watercolor", z_index=2),
        
        # Bottom Horizontal
        PhotoPlacement(x=100, y=2400, width=1700, height=500, rotation=0, 
                      frame_style="none", filter="luxury", z_index=3),
        
        # Accent Square
        PhotoPlacement(x=1900, y=1650, width=950, height=1250, rotation=0, 
                      frame_style="border", filter="vibrant", z_index=4),
    ]
    
    return CollageTemplate(
        name="Moodboard",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        background_type="solid",
        background_colors=["#F8F9FA"],
        placements=placements[:num_photos],
        decorations=[
            {"type": "text", "content": "AESTHETIC STUDIO", "x": 100, "y": 2850, "font_size": 120, "color": "#636E72"}
        ]
    )


# ============================================================================
# TEMPLATE 4: EXPERT FILMSTRIP (Cinematic Sequences)
# ============================================================================
def get_filmstrip_template(num_photos: int) -> CollageTemplate:
    """
    Expert Filmstrip: Ultra-HD Cinematic Vertical Sequence (3000px)
    """
    canvas_w, canvas_h = 3000, 4200
    placements = [
        PhotoPlacement(x=200, y=200, width=2600, height=1200, rotation=0, 
                      filter="luxury", z_index=1, no_shadow=True),
        
        PhotoPlacement(x=200, y=1500, width=2600, height=1200, rotation=0, 
                      filter="vintage", z_index=2, no_shadow=True),
        
        PhotoPlacement(x=200, y=2800, width=2600, height=1200, rotation=0, 
                      filter="luxury", z_index=3, no_shadow=True),
    ]
    
    decorations = [
        {"type": "text", "content": "KODAK PORTRA 400", "x": 2300, "y": 4100, "font_size": 60, "color": "#E67E22"},
        {"type": "text", "content": "SCENE 001", "x": 200, "y": 4100, "font_size": 60, "color": "#FFFFFF"},
    ]
    
    return CollageTemplate(
        name="Filmstrip",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        background_type="solid",
        background_colors=["#000000"],
        placements=placements[:num_photos],
        decorations=decorations
    )


def get_doodle_template(num_photos: int) -> CollageTemplate:
    """
    Expert Doodle: Ultra-HD Playful Sticker Layout (3000px)
    """
    canvas_w, canvas_h = 3000, 3000
    placements = [
        # Main Sticker
        PhotoPlacement(x=500, y=500, width=2000, height=2000, rotation=-3, 
                      frame_style="none", filter="vibrant", z_index=5, use_cutout=True),
        
        # Supporting Photo
        PhotoPlacement(x=100, y=1800, width=1200, height=1100, rotation=6, 
                      frame_style="border", filter="soft", z_index=2),
        
        # Accent Photo
        PhotoPlacement(x=1700, y=1800, width=1200, height=1100, rotation=-6, 
                      frame_style="border", filter="vibrant", z_index=3),
    ]
    
    decorations = [
        {"type": "doodle", "shape": "heart", "x": 2400, "y": 400, "size": 350, "color": "#FF6B6B"},
        {"type": "doodle", "shape": "star", "x": 400, "y": 400, "size": 300, "color": "#F1C40F"},
        {"type": "text", "content": "STAY WILD", "x": 800, "y": 2750, "font_size": 280, "color": "#FC5C65"},
    ]
    
    return CollageTemplate(
        name="Doodle",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        background_type="solid",
        background_colors=["#FFF9FF"],
        placements=placements[:num_photos],
        decorations=decorations
    )


# ============================================================================
# TEMPLATE 6: EXPERT STICKER (Cutout Collage)
# ============================================================================
def get_sticker_collage_template(num_photos: int) -> CollageTemplate:
    """
    Expert Sticker: Ultra-HD Dense Cutout Layout (3000px Vertical)
    Optimized for ALL cutouts, no frames, and playful decorations.
    """
    canvas_w, canvas_h = 2400, 3800
    
    # Dense, overlapping slots for a "messy but aesthetic" look
    placements = [
        # Center-Left (Hero)
        PhotoPlacement(x=100, y=100, width=1400, height=1800, rotation=-5, 
                      use_cutout=True, use_outline=True, outline_width=45, z_index=10),
        
        # Top-Right
        PhotoPlacement(x=1200, y=50, width=1100, height=1300, rotation=4, 
                      use_cutout=True, use_outline=True, outline_width=35, z_index=2),
        
        # Bottom-Right
        PhotoPlacement(x=1150, y=1900, width=1200, height=1700, rotation=-6, 
                      use_cutout=True, use_outline=True, outline_width=40, z_index=15),
        
        # Bottom-Left
        PhotoPlacement(x=50, y=2100, width=1100, height=1400, rotation=8, 
                      use_cutout=True, use_outline=True, outline_width=35, z_index=5),
        
        # Middle-Right (Floating)
        PhotoPlacement(x=1300, y=1200, width=1000, height=1200, rotation=-12, 
                      use_cutout=True, use_outline=True, outline_width=30, z_index=12),
        
        # Middle-Left (Floating)
        PhotoPlacement(x=50, y=1400, width=900, height=1100, rotation=15, 
                      use_cutout=True, use_outline=True, outline_width=30, z_index=3),
    ]
    
    # Add more decorations for "Cute" factor
    decorations = [
        {"type": "doodle", "shape": "heart", "x": 100, "y": 100, "size": 150, "color": "#FF6B6B"},
        {"type": "doodle", "shape": "star", "x": 2200, "y": 150, "size": 180, "color": "#F1C40F"},
        {"type": "doodle", "shape": "squiggle", "x": 1200, "y": 1700, "size": 400, "color": "#FFFFFF"},
        {"type": "doodle", "shape": "heart", "x": 2300, "y": 3400, "size": 200, "color": "#FF6B6B"},
        {"type": "doodle", "shape": "star", "x": 150, "y": 3600, "size": 180, "color": "#F1C40F"},
        {"type": "doodle", "shape": "heart", "x": 1200, "y": 400, "size": 120, "color": "#FC5C65"},
        {"type": "doodle", "shape": "squiggle", "x": 200, "y": 1400, "size": 250, "color": "#F1C40F"},
        
        # Smaller, aesthetic text captions
        {"type": "text", "content": "#VIBES", "x": 1200, "y": 3650, "font_size": 80, "color": "#2F3640"},
        {"type": "text", "content": "✨ STORY ✨", "x": 100, "y": 3650, "font_size": 80, "color": "#2F3640"},
        {"type": "text", "content": "LOVELY", "x": 1800, "y": 3650, "font_size": 90, "color": "#FC5C65"},
        {"type": "text", "content": "CUTIE", "x": 1500, "y": 100, "font_size": 100, "color": "#F1C40F"},
    ]
    
    return CollageTemplate(
        name="Sticker",
        canvas_width=canvas_w,
        canvas_height=canvas_h,
        background_type="solid",
        background_colors=["#F8F9FA"],
        placements=placements[:num_photos],
        decorations=decorations
    )


# ============================================================================
# TEMPLATE SELECTOR
# ============================================================================
def get_template_by_style(style: str, num_photos: int) -> CollageTemplate:
    """
    Select appropriate template based on detected style/emotion
    """
    style = style.lower()
    
    if "sticker" in style or "cutout" in style or "scrapbook" in style or "memory" in style:
        return get_sticker_collage_template(num_photos)
    elif "magazine" in style or "editorial" in style or "fashion" in style:
        return get_magazine_template(num_photos)
    elif "mood" in style or "aesthetic" in style or "pinterest" in style:
        return get_moodboard_template(num_photos)
    elif "film" in style or "story" in style or "sequence" in style:
        return get_filmstrip_template(num_photos)
    elif "doodle" in style or "fun" in style or "playful" in style:
        return get_doodle_template(num_photos)
    elif "sticker" in style or "cutout" in style:
        return get_sticker_collage_template(num_photos)
    else:
        # Default to mood board for versatility
        return get_moodboard_template(num_photos)
