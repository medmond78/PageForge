# tests/test_images.py
import pytest
from pathlib import Path
from pageforge.images import resolve_image, validate_image, load_raster_image
from pageforge.config import ImageConfig


def test_resolve_image_relative_path():
    markdown_dir = Path("tests/fixtures")
    config = ImageConfig()

    result = resolve_image("test-image.png", markdown_dir, config, interactive=False)
    assert result is not None
    assert result.name == "test-image.png"
    assert result.exists()


def test_resolve_image_not_found():
    markdown_dir = Path("tests/fixtures")
    config = ImageConfig()

    result = resolve_image("nonexistent.png", markdown_dir, config, interactive=False)
    assert result is None


def test_validate_image_valid_png():
    path = Path("tests/fixtures/test-image.png")
    assert validate_image(path) is True


def test_validate_image_valid_svg():
    path = Path("tests/fixtures/test-diagram.svg")
    assert validate_image(path) is True


def test_validate_image_not_exists():
    path = Path("tests/fixtures/nonexistent.png")
    assert validate_image(path) is False


def test_load_raster_image():
    path = Path("tests/fixtures/test-image.png")
    config = ImageConfig()

    img = load_raster_image(path, config)
    assert img is not None
    assert hasattr(img, 'drawWidth')
    assert hasattr(img, 'drawHeight')
