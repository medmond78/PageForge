# pageforge/images.py
"""Image resolution and loading for PageForge."""

from pathlib import Path
from typing import Optional

from PIL import Image
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage
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
    """Resolve image path with fallback strategy."""
    # Try relative to markdown file
    relative_path = markdown_dir / image_ref
    if validate_image(relative_path):
        return relative_path

    # Try fallback directory if configured
    if config.fallback_dir:
        fallback_path = Path(config.fallback_dir) / image_ref
        if validate_image(fallback_path):
            return fallback_path

    # TODO: Interactive prompt in future task
    # For now, return None if not found
    return None


def load_raster_image(path: Path, config: ImageConfig) -> RLImage:
    """Load PNG/JPG image with size constraints."""
    # Open image to get dimensions
    with Image.open(path) as img:
        width_px, height_px = img.size

    # Convert to inches at configured DPI
    width_in = width_px / config.dpi
    height_in = height_px / config.dpi

    # Scale down if exceeds max dimensions
    if width_in > config.max_width:
        scale = config.max_width / width_in
        width_in = config.max_width
        height_in = height_in * scale

    if height_in > config.max_height:
        scale = config.max_height / height_in
        height_in = config.max_height
        width_in = width_in * scale

    # Create ReportLab image
    img = RLImage(str(path), width=width_in * inch, height=height_in * inch)
    return img


def load_svg_image(path: Path, config: ImageConfig):
    """Load SVG and convert to ReportLab drawing."""
    drawing = svg2rlg(str(path))
    if drawing is None:
        return None

    # Scale to fit max dimensions
    scale_x = (config.max_width * inch) / drawing.width if drawing.width > 0 else 1
    scale_y = (config.max_height * inch) / drawing.height if drawing.height > 0 else 1
    scale = min(scale_x, scale_y, 1.0)  # Don't upscale

    drawing.width = drawing.width * scale
    drawing.height = drawing.height * scale
    drawing.scale(scale, scale)

    return drawing
