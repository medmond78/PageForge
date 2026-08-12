# pageforge/images.py
"""Image resolution and loading for PageForge."""

from pathlib import Path
from typing import Optional

from PIL import Image
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage
from reportlab.graphics.shapes import Drawing
from svglib.svglib import svg2rlg

from pageforge.config import ImageConfig


def validate_image(path: Path) -> bool:
    """Check if image file exists and is valid format."""
    if not path.exists():
        return False

    suffix = path.suffix.lower()
    if suffix in [".png", ".jpg", ".jpeg"]:
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except Exception:
            return False
    elif suffix == ".svg":
        return True  # SVG validation happens at load time

    return False


def resolve_image(
    image_ref: str,
    markdown_dir: Path,
    config: ImageConfig,
    interactive: bool = True
) -> Optional[Path]:
    """Resolve image path with fallback strategy.

    Args:
        image_ref: Image reference from markdown
        markdown_dir: Directory containing the markdown file
        config: Image configuration
        interactive: If True, prompt user for missing images

    Returns:
        Path to resolved image, or None if not found
    """
    # Try relative to markdown file
    relative_path = markdown_dir / image_ref
    if validate_image(relative_path):
        return relative_path

    # Try fallback directory if configured
    if config.fallback_dir:
        fallback_path = Path(config.fallback_dir) / image_ref
        if validate_image(fallback_path):
            return fallback_path

    # Interactive prompt if enabled
    if interactive:
        user_path = input(f"Image not found: {image_ref}. Enter path or leave blank to skip: ")
        if user_path:
            user_path_obj = Path(user_path)
            if validate_image(user_path_obj):
                return user_path_obj

    # Not found
    return None


def load_raster_image(path: Path, config: ImageConfig) -> RLImage:
    """Load PNG/JPG image with size constraints."""
    # Open image to get dimensions
    with Image.open(path) as img:
        width_px, height_px = img.size

    # Convert to inches at configured DPI
    width_in = width_px / config.dpi
    height_in = height_px / config.dpi

    # Calculate scale factors (don't upscale)
    width_scale = config.max_width / width_in if width_in > config.max_width else 1.0
    height_scale = config.max_height / height_in if height_in > config.max_height else 1.0
    scale = min(width_scale, height_scale)

    # Apply scale once
    width_in *= scale
    height_in *= scale

    # Create ReportLab image
    img = RLImage(str(path), width=width_in * inch, height=height_in * inch)
    return img


def load_svg_image(path: Path, config: ImageConfig) -> Optional[Drawing]:
    """Load SVG and convert to ReportLab drawing."""
    try:
        drawing = svg2rlg(str(path))
        if drawing is None:
            return None
    except Exception:
        return None

    # Scale to fit max dimensions
    scale_x = (config.max_width * inch) / drawing.width if drawing.width > 0 else 1
    scale_y = (config.max_height * inch) / drawing.height if drawing.height > 0 else 1
    scale = min(scale_x, scale_y, 1.0)  # Don't upscale

    drawing.width = drawing.width * scale
    drawing.height = drawing.height * scale
    drawing.scale(scale, scale)

    return drawing
