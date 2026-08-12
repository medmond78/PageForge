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

    flowables = html_to_flowables(html, styles, config, markdown_dir, {})
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)


def test_html_to_flowables_heading():
    config = get_default_config()
    styles = get_styles(config)
    html = "<h1>Heading 1</h1>"
    markdown_dir = Path(".")

    flowables = html_to_flowables(html, styles, config, markdown_dir, {})
    assert len(flowables) > 0
    assert isinstance(flowables[0], Paragraph)


def test_html_to_flowables_list():
    config = get_default_config()
    styles = get_styles(config)
    html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
    markdown_dir = Path(".")

    flowables = html_to_flowables(html, styles, config, markdown_dir, {})
    assert len(flowables) > 0


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

    generate_pdf(doc, output_path, config, {})

    assert output_path.exists()
    assert output_path.stat().st_size > 0
