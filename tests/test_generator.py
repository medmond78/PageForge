# tests/test_generator.py
import pytest
from pathlib import Path
from reportlab.platypus import Paragraph, Spacer, Image as RLImage
from pageforge.generator import html_to_flowables, generate_pdf
from pageforge.config import get_default_config
from pageforge.styles import get_styles
from pageforge.parser import parse_markdown


def test_html_to_flowables_paragraph():
    config = get_default_config()
    styles = get_styles(config)
    html = "<p>Simple paragraph</p>"
    markdown_dir = Path(".")

    flowables, missing_count = html_to_flowables(html, styles, config, markdown_dir, {}, interactive=False)
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)
    assert missing_count == 0


def test_html_to_flowables_heading():
    config = get_default_config()
    styles = get_styles(config)
    html = "<h1>Heading 1</h1>"
    markdown_dir = Path(".")

    flowables, missing_count = html_to_flowables(html, styles, config, markdown_dir, {}, interactive=False)
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)
    assert missing_count == 0


def test_html_to_flowables_list():
    config = get_default_config()
    styles = get_styles(config)
    html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
    markdown_dir = Path(".")

    flowables, missing_count = html_to_flowables(html, styles, config, markdown_dir, {}, interactive=False)
    assert len(flowables) > 0
    assert missing_count == 0


def test_generate_pdf_integration(tmp_path):
    config = get_default_config()
    content = """# Test Document

This is a test paragraph.

## Section 1

- Item 1
- Item 2
"""
    doc = parse_markdown(content, Path("."))
    output_path = tmp_path / "test.pdf"

    missing_count = generate_pdf(doc, output_path, config, {}, interactive=False)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
    assert missing_count == 0


def test_html_to_flowables_image_zero_dimensions(tmp_path, monkeypatch):
    """Test handling of images with zero dimensions (should not crash with ZeroDivisionError)."""
    from unittest.mock import MagicMock

    config = get_default_config()
    styles = get_styles(config)

    # Create a real image file to pass existence checks
    from PIL import Image as PILImage
    test_image = tmp_path / "test.png"
    img = PILImage.new('RGB', (10, 10), color='blue')
    img.save(test_image)

    # Mock RLImage to have zero width
    original_rlimage = RLImage
    def mock_rlimage(path):
        img = original_rlimage(path)
        img.imageWidth = 0
        img.imageHeight = 100
        return img

    monkeypatch.setattr('pageforge.generator.RLImage', mock_rlimage)

    html = f'<img src="{test_image}" alt="Zero width image"/>'

    # Should not raise ZeroDivisionError
    flowables, missing_count = html_to_flowables(html, styles, config, tmp_path, {}, interactive=False)

    # Should have a warning paragraph for image load error
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)
    assert missing_count == 0  # Image exists, just has zero dimensions


def test_html_to_flowables_image_invalid_file(tmp_path):
    """Test handling of corrupted/invalid image files."""
    config = get_default_config()
    styles = get_styles(config)

    # Create an invalid image file (just text)
    invalid_image = tmp_path / "invalid.png"
    invalid_image.write_text("This is not an image")

    html = f'<img src="{invalid_image}" alt="Invalid image"/>'

    # Should not crash, should handle gracefully
    flowables, missing_count = html_to_flowables(html, styles, config, tmp_path, {}, interactive=False)

    # Should have a warning paragraph
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)
    assert missing_count == 1  # Invalid image counts as missing


def test_html_to_flowables_image_missing_file(tmp_path):
    """Test handling of missing image files."""
    config = get_default_config()
    styles = get_styles(config)

    # Reference non-existent file
    html = '<img src="nonexistent.png" alt="Missing image"/>'

    flowables, missing_count = html_to_flowables(html, styles, config, tmp_path, {}, interactive=False)

    # Should have a warning paragraph
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)
    assert missing_count == 1  # Missing image should be counted
