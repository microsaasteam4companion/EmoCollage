"""
Collage Template Definitions
Pinterest-inspired layouts with precise positioning and styling
"""

from typing import List, Dict, Tuple, Any
from dataclasses import dataclass


@dataclass
class PhotoPlacement:
    """Defines how a photo should be placed in the template"""
    x: int  # X position
    y: int  # Y position
    width: int  # Width
    height: int  # Height
    rotation: float = 0  # Rotation angle in degrees
    frame_style: str = "none"  # none, polaroid, border
    filter: str = "none"  # Filter to apply
    z_index: int = 0  # Layer order


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
    Scattered polaroid-style photos with washi tape and doodles
    Perfect for: Memories, casual moments, fun vibes
    """
    placements = [
        PhotoPlacement(x=100, y=150, width=400, height=500, rotation=-5, 
                      frame_style="polaroid", filter="vintage", z_index=2),
        PhotoPlacement(x=550, y=100, width=350, height=450, rotation=8, 
                      frame_style="polaroid", filter="soft", z_index=3),
        PhotoPlacement(x=200, y=700, width=380, height=480, rotation=-3, 
                      frame_style="polaroid", filter="none", z_index=1),
        PhotoPlacement(x=650, y=650, width=400, height=500, rotation=6, 
                      frame_style="polaroid", filter="warm", z_index=4),
    ]
    
    decorations = [
        {"type": "washi_tape", "x": 120, "y": 130, "rotation": -5, "color": "#FFB6C1"},
        {"type": "washi_tape", "x": 570, "y": 80, "rotation": 8, "color": "#98D8C8"},
        {"type": "doodle", "shape": "heart", "x": 900, "y": 200, "size": 60},
        {"type": "doodle", "shape": "star", "x": 150, "y": 1100, "size": 50},
    ]
    
    return CollageTemplate(
        name="Scrapbook",
        canvas_width=1200,
        canvas_height=1400,
        background_type="solid",
        background_colors=["#FFF8F0"],
        placements=placements[:num_photos],
        decorations=decorations
    )


# ============================================================================
# TEMPLATE 2: MAGAZINE EDITORIAL
# ============================================================================
def get_magazine_template(num_photos: int) -> CollageTemplate:
    """
    Clean, professional layout with hero image and accents
    Perfect for: Fashion, portraits, professional shots
    """
    placements = [
        # Hero image - large and centered
        PhotoPlacement(x=100, y=100, width=700, height=900, rotation=0, 
                      frame_style="none", filter="luxury", z_index=1),
        # Accent 1 - top right
        PhotoPlacement(x=850, y=100, width=300, height=400, rotation=0, 
                      frame_style="border", filter="bw", z_index=2),
        # Accent 2 - bottom right
        PhotoPlacement(x=850, y=550, width=300, height=400, rotation=0, 
                      frame_style="border", filter="none", z_index=2),
    ]
    
    decorations = [
        {"type": "text", "content": "EDITORIAL", "x": 100, "y": 1050, 
         "font_size": 48, "color": "#000000"},
    ]
    
    return CollageTemplate(
        name="Magazine",
        canvas_width=1200,
        canvas_height=1400,
        background_type="solid",
        background_colors=["#FFFFFF"],
        placements=placements[:num_photos],
        decorations=decorations
    )


# ============================================================================
# TEMPLATE 3: MOOD BOARD
# ============================================================================
def get_moodboard_template(num_photos: int) -> CollageTemplate:
    """
    Asymmetric grid with overlapping elements
    Perfect for: Inspiration, aesthetics, color stories
    """
    placements = [
        PhotoPlacement(x=50, y=50, width=500, height=600, rotation=-2, 
                      frame_style="none", filter="vibrant", z_index=1),
        PhotoPlacement(x=450, y=200, width=400, height=500, rotation=3, 
                      frame_style="none", filter="none", z_index=2),
        PhotoPlacement(x=100, y=700, width=350, height=450, rotation=-4, 
                      frame_style="none", filter="soft", z_index=3),
        PhotoPlacement(x=500, y=750, width=450, height=550, rotation=2, 
                      frame_style="none", filter="warm", z_index=4),
        PhotoPlacement(x=900, y=100, width=250, height=300, rotation=-3, 
                      frame_style="polaroid", filter="vintage", z_index=5),
    ]
    
    decorations = [
        {"type": "color_swatch", "x": 1000, "y": 500, "colors": []},  # Will be filled with palette
    ]
    
    return CollageTemplate(
        name="Moodboard",
        canvas_width=1200,
        canvas_height=1400,
        background_type="gradient",
        background_colors=["#F5F5F5", "#E8E8E8"],
        placements=placements[:num_photos],
        decorations=decorations
    )


# ============================================================================
# TEMPLATE 4: FILM STRIP
# ============================================================================
def get_filmstrip_template(num_photos: int) -> CollageTemplate:
    """
    Horizontal or vertical film strip with borders
    Perfect for: Sequences, stories, before/after
    """
    # Vertical strip
    spacing = 50
    photo_height = 350
    start_y = 100
    
    placements = []
    for i in range(min(num_photos, 4)):
        placements.append(
            PhotoPlacement(
                x=300, 
                y=start_y + (i * (photo_height + spacing)),
                width=600, 
                height=photo_height,
                rotation=0,
                frame_style="border",
                filter="bw" if i % 2 == 0 else "none",
                z_index=i
            )
        )
    
    decorations = [
        {"type": "film_holes", "side": "left"},
        {"type": "film_holes", "side": "right"},
    ]
    
    return CollageTemplate(
        name="FilmStrip",
        canvas_width=1200,
        canvas_height=1600,
        background_type="solid",
        background_colors=["#1a1a1a"],
        placements=placements,
        decorations=decorations
    )


# ============================================================================
# TEMPLATE 5: DOODLE ART
# ============================================================================
def get_doodle_template(num_photos: int) -> CollageTemplate:
    """
    Playful layout with hand-drawn elements and stickers
    Perfect for: Fun, casual, youthful vibes
    """
    placements = [
        PhotoPlacement(x=150, y=200, width=350, height=450, rotation=-8, 
                      frame_style="polaroid", filter="vibrant", z_index=2),
        PhotoPlacement(x=600, y=150, width=400, height=500, rotation=5, 
                      frame_style="polaroid", filter="none", z_index=3),
        PhotoPlacement(x=250, y=750, width=350, height=450, rotation=-4, 
                      frame_style="polaroid", filter="warm", z_index=1),
        PhotoPlacement(x=700, y=800, width=380, height=480, rotation=7, 
                      frame_style="polaroid", filter="soft", z_index=4),
    ]
    
    decorations = [
        {"type": "doodle", "shape": "star", "x": 100, "y": 100, "size": 80, "color": "#FFD700"},
        {"type": "doodle", "shape": "heart", "x": 1000, "y": 300, "size": 70, "color": "#FF69B4"},
        {"type": "doodle", "shape": "circle", "x": 200, "y": 1200, "size": 60, "color": "#87CEEB"},
        {"type": "doodle", "shape": "squiggle", "x": 900, "y": 1100, "size": 100, "color": "#98D8C8"},
        {"type": "text", "content": "✨", "x": 500, "y": 50, "font_size": 60},
    ]
    
    return CollageTemplate(
        name="Doodle",
        canvas_width=1200,
        canvas_height=1400,
        background_type="solid",
        background_colors=["#FFF9E6"],
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
    
    if "scrapbook" in style or "memory" in style or "casual" in style:
        return get_scrapbook_template(num_photos)
    elif "magazine" in style or "editorial" in style or "fashion" in style:
        return get_magazine_template(num_photos)
    elif "mood" in style or "aesthetic" in style or "pinterest" in style:
        return get_moodboard_template(num_photos)
    elif "film" in style or "story" in style or "sequence" in style:
        return get_filmstrip_template(num_photos)
    elif "doodle" in style or "fun" in style or "playful" in style:
        return get_doodle_template(num_photos)
    else:
        # Default to mood board for versatility
        return get_moodboard_template(num_photos)
