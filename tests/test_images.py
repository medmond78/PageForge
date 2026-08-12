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


def test_load_svg_image():
    from pageforge.images import load_svg_image
    path = Path("tests/fixtures/test-diagram.svg")
    config = ImageConfig()

    drawing = load_svg_image(path, config)
    assert drawing is not None
    assert hasattr(drawing, 'width')
    assert hasattr(drawing, 'height')


def test_resolve_image_interactive_with_valid_user_path(mocker, tmp_path):
    """Test interactive mode where user provides valid image path."""
    # Create valid image
    valid_image = tmp_path / "user_image.png"
    from PIL import Image
    img = Image.new('RGB', (50, 50), color='green')
    img.save(valid_image)

    markdown_dir = tmp_path
    config = ImageConfig()

    # Mock input to return valid path
    mock_input = mocker.patch('builtins.input', return_value=str(valid_image))

    result = resolve_image("missing.png", markdown_dir, config, interactive=True)

    # Should have prompted user and returned the valid path
    mock_input.assert_called_once()
    assert 'Image not found: missing.png' in mock_input.call_args[0][0]
    assert result == valid_image


def test_resolve_image_interactive_with_blank_input(mocker, tmp_path):
    """Test interactive mode where user skips (blank input)."""
    markdown_dir = tmp_path
    config = ImageConfig()

    # Mock input to return blank
    mock_input = mocker.patch('builtins.input', return_value='')

    result = resolve_image("missing.png", markdown_dir, config, interactive=True)

    # Should have prompted user and returned None
    mock_input.assert_called_once()
    assert result is None


def test_resolve_image_interactive_with_invalid_user_path(mocker, tmp_path):
    """Test interactive mode where user provides invalid path."""
    markdown_dir = tmp_path
    config = ImageConfig()

    # Mock input to return invalid path
    mock_input = mocker.patch('builtins.input', return_value='/nonexistent/invalid.png')

    result = resolve_image("missing.png", markdown_dir, config, interactive=True)

    # Should have prompted user and returned None (invalid path)
    mock_input.assert_called_once()
    assert result is None


def test_resolve_image_non_interactive_no_prompt(mocker, tmp_path):
    """Test non-interactive mode doesn't prompt user."""
    markdown_dir = tmp_path
    config = ImageConfig()

    # Mock input - should NOT be called
    mock_input = mocker.patch('builtins.input')

    result = resolve_image("missing.png", markdown_dir, config, interactive=False)

    # Should NOT have prompted user
    mock_input.assert_not_called()
    assert result is None
