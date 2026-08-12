# tests/test_parser.py
import pytest
from pathlib import Path
from pageforge.parser import parse_markdown, extract_frontmatter, find_image_references


def test_extract_frontmatter():
    content = """---
title: Test
author: Me
---

# Content
"""
    metadata, body = extract_frontmatter(content)
    assert metadata["title"] == "Test"
    assert metadata["author"] == "Me"
    assert "# Content" in body


def test_extract_frontmatter_no_frontmatter():
    content = "# Just Content"
    metadata, body = extract_frontmatter(content)
    assert metadata == {}
    assert body == "# Just Content"


def test_parse_markdown_basic():
    content = "# Heading\n\nParagraph"
    doc = parse_markdown(content, Path("."))
    assert doc.metadata == {}
    assert doc.html is not None
    assert "<h1>Heading</h1>" in doc.html
    assert "<p>Paragraph</p>" in doc.html


def test_parse_markdown_with_frontmatter():
    content = """---
title: Test
---

# Content
"""
    doc = parse_markdown(content, Path("."))
    assert doc.metadata["title"] == "Test"
    assert "Content" in doc.html


def test_find_image_references():
    html = '<p><img src="image1.png" alt="Alt1" /></p><p><img src="image2.svg" alt="Alt2" /></p>'
    images = find_image_references(html)
    assert len(images) == 2
    assert images[0]["src"] == "image1.png"
    assert images[0]["alt"] == "Alt1"
    assert images[1]["src"] == "image2.svg"


def test_parse_markdown_integration():
    fixture = Path("tests/fixtures/basic.md")
    content = fixture.read_text()
    doc = parse_markdown(content, fixture.parent)

    assert doc.metadata["title"] == "Test Document"
    assert len(doc.images) == 1
    assert doc.images[0]["src"] == "test-image.png"
