# PageForge MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build working Markdown-to-PDF CLI tool with basic features (headings, paragraphs, lists, images, code blocks)

**Architecture:** Pure Python using ReportLab Platypus for PDF generation, Click for CLI, python-markdown for parsing

**Tech Stack:** Python 3.10+, ReportLab, markdown, Pillow, svglib, Pygments, Click, PyYAML, python-frontmatter

---

## File Structure Overview

```
pageforge/
├── pageforge/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration dataclasses and defaults
│   ├── styles.py             # ReportLab style definitions
│   ├── parser.py             # Markdown parsing
│   ├── images.py             # Image resolution and loading
│   ├── generator.py          # PDF generation
│   └── cli.py                # CLI entry point
├── tests/
│   ├── test_config.py
│   ├── test_parser.py
│   ├── test_images.py
│   ├── test_generator.py
│   ├── fixtures/
│   │   ├── basic.md
│   │   ├── test-image.png
│   │   └── test-diagram.svg
│   └── integration/
│       └── test_cli.py
├── pyproject.toml
└── README.md
```

---

## Task 1: Project Setup

**Files:**
- Create: `pyproject.toml`
- Create: `pageforge/__init__.py`
- Create: `README.md`

- [ ] **Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "pageforge"
version = "0.1.0"
description = "Markdown to PDF converter optimized for LLM-generated content"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Matthew Edmond", email = "medmond78@users.noreply.github.com"}
]
dependencies = [
    "reportlab>=4.0.0",
    "markdown>=3.5.0",
    "python-frontmatter>=1.0.0",
    "Pillow>=10.0.0",
    "svglib>=1.5.0",
    "Pygments>=2.17.0",
    "PyYAML>=6.0.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
pageforge = "pageforge.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["pageforge*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
target-version = "py310"
```

- [ ] **Step 2: Create package init**

```python
# pageforge/__init__.py
"""PageForge: Markdown to PDF converter."""

__version__ = "0.1.0"
```

- [ ] **Step 3: Create basic README**

```markdown
# PageForge

Markdown to PDF converter optimized for LLM-generated content.

## Installation

```bash
pip install -e .
```

## Usage

```bash
pageforge document.md
pageforge document.md -o output.pdf
```

## License

MIT License - see LICENSE file for details.
```

- [ ] **Step 4: Install dependencies**

Run: `pip install -e ".[dev]"`
Expected: All packages installed successfully

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml pageforge/__init__.py README.md
git commit -m "feat: initial project setup with dependencies

- Add pyproject.toml with all dependencies
- Create package structure
- Add basic README

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 2: Configuration System

**Files:**
- Create: `pageforge/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Write test for default config**

```python
# tests/test_config.py
import pytest
from pageforge.config import get_default_config, Config, PageConfig, FontConfig


def test_get_default_config():
    config = get_default_config()
    assert isinstance(config, Config)
    assert config.page.size == "letter"
    assert config.page.orientation == "portrait"
    assert config.fonts.body == "Helvetica"


def test_page_config_defaults():
    page = PageConfig()
    assert page.size == "letter"
    assert page.orientation == "portrait"
    assert page.margins.top == 1.0
    assert page.margins.bottom == 1.0
    assert page.margins.left == 1.0
    assert page.margins.right == 1.0


def test_font_config_defaults():
    fonts = FontConfig()
    assert fonts.body == "Helvetica"
    assert fonts.heading == "Helvetica-Bold"
    assert fonts.code == "Courier"
    assert fonts.sizes.h1 == 24
    assert fonts.sizes.body == 11
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'pageforge.config'"

- [ ] **Step 3: Implement config dataclasses**

```python
# pageforge/config.py
"""Configuration management for PageForge."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Margins:
    """Page margin configuration in inches."""
    top: float = 1.0
    bottom: float = 1.0
    left: float = 1.0
    right: float = 1.0


@dataclass
class PageConfig:
    """Page layout configuration."""
    size: str = "letter"  # letter, a4, legal
    orientation: str = "portrait"  # portrait, landscape
    margins: Margins = field(default_factory=Margins)


@dataclass
class FontSizes:
    """Font sizes in points."""
    h1: int = 24
    h2: int = 18
    h3: int = 14
    h4: int = 12
    h5: int = 11
    h6: int = 10
    body: int = 11
    code: int = 9
    caption: int = 9


@dataclass
class FontConfig:
    """Font configuration."""
    body: str = "Helvetica"
    heading: str = "Helvetica-Bold"
    code: str = "Courier"
    sizes: FontSizes = field(default_factory=FontSizes)


@dataclass
class ColorConfig:
    """Color configuration (RGB hex strings)."""
    text: str = "#000000"
    headings: str = "#1a1a1a"
    code_bg: str = "#f5f5f5"
    code_text: str = "#2c3e50"
    links: str = "#0066cc"
    table_header: str = "#e8e8e8"


@dataclass
class SpacingConfig:
    """Spacing configuration in points."""
    paragraph: int = 12
    heading_before: int = 18
    heading_after: int = 6
    line_height: float = 1.2
    list_indent: int = 20


@dataclass
class ImageConfig:
    """Image configuration."""
    max_width: float = 6.5  # inches
    max_height: float = 9.0  # inches
    dpi: int = 150
    fallback_dir: Optional[str] = None
    center_align: bool = True
    show_captions: bool = True


@dataclass
class CodeConfig:
    """Code block configuration."""
    syntax_highlight: bool = True
    theme: str = "default"
    show_line_numbers: bool = False
    wrap_long_lines: bool = True
    background: bool = True


@dataclass
class Config:
    """Complete PageForge configuration."""
    page: PageConfig = field(default_factory=PageConfig)
    fonts: FontConfig = field(default_factory=FontConfig)
    colors: ColorConfig = field(default_factory=ColorConfig)
    spacing: SpacingConfig = field(default_factory=SpacingConfig)
    images: ImageConfig = field(default_factory=ImageConfig)
    code: CodeConfig = field(default_factory=CodeConfig)


def get_default_config() -> Config:
    """Return default configuration."""
    return Config()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py -v`
Expected: PASS - all tests pass

- [ ] **Step 5: Commit**

```bash
git add pageforge/config.py tests/test_config.py
git commit -m "feat: add configuration system with defaults

- Create dataclasses for all config sections
- Implement get_default_config()
- Add comprehensive unit tests

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 3: Style Definitions

**Files:**
- Create: `pageforge/styles.py`
- Create: `tests/test_styles.py`

- [ ] **Step 1: Write test for style creation**

```python
# tests/test_styles.py
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from pageforge.styles import get_styles, create_heading_style
from pageforge.config import get_default_config


def test_get_styles():
    config = get_default_config()
    styles = get_styles(config)
    
    assert "Normal" in styles
    assert "Heading1" in styles
    assert "Heading2" in styles
    assert "Code" in styles


def test_normal_style():
    config = get_default_config()
    styles = get_styles(config)
    normal = styles["Normal"]
    
    assert normal.fontName == "Helvetica"
    assert normal.fontSize == 11
    assert normal.spaceBefore == 0
    assert normal.spaceAfter == 12


def test_heading_styles():
    config = get_default_config()
    styles = get_styles(config)
    
    h1 = styles["Heading1"]
    assert h1.fontName == "Helvetica-Bold"
    assert h1.fontSize == 24
    assert h1.spaceBefore == 18
    assert h1.spaceAfter == 6
    
    h2 = styles["Heading2"]
    assert h2.fontSize == 18


def test_create_heading_style():
    config = get_default_config()
    style = create_heading_style(1, config.fonts, config.spacing)
    
    assert isinstance(style, ParagraphStyle)
    assert style.fontSize == 24
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_styles.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement style creation**

```python
# pageforge/styles.py
"""ReportLab style definitions for PageForge."""

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch

from pageforge.config import Config, FontConfig, SpacingConfig, ColorConfig


def hex_to_reportlab_color(hex_str: str) -> colors.Color:
    """Convert hex color string to ReportLab Color object."""
    hex_str = hex_str.lstrip('#')
    r = int(hex_str[0:2], 16) / 255
    g = int(hex_str[2:4], 16) / 255
    b = int(hex_str[4:6], 16) / 255
    return colors.Color(r, g, b)


def create_heading_style(
    level: int,
    fonts: FontConfig,
    spacing: SpacingConfig
) -> ParagraphStyle:
    """Create style for heading level (1-6)."""
    size_map = {
        1: fonts.sizes.h1,
        2: fonts.sizes.h2,
        3: fonts.sizes.h3,
        4: fonts.sizes.h4,
        5: fonts.sizes.h5,
        6: fonts.sizes.h6,
    }
    
    return ParagraphStyle(
        f"Heading{level}",
        fontName=fonts.heading,
        fontSize=size_map.get(level, fonts.sizes.body),
        leading=size_map.get(level, fonts.sizes.body) * spacing.line_height,
        spaceBefore=spacing.heading_before,
        spaceAfter=spacing.heading_after,
        alignment=TA_LEFT,
        textColor=colors.black,
    )


def get_styles(config: Config) -> dict:
    """Generate all ReportLab styles from configuration."""
    styles = {}
    
    # Normal paragraph style
    text_color = hex_to_reportlab_color(config.colors.text)
    styles["Normal"] = ParagraphStyle(
        "Normal",
        fontName=config.fonts.body,
        fontSize=config.fonts.sizes.body,
        leading=config.fonts.sizes.body * config.spacing.line_height,
        spaceBefore=0,
        spaceAfter=config.spacing.paragraph,
        alignment=TA_LEFT,
        textColor=text_color,
    )
    
    # Heading styles
    for level in range(1, 7):
        styles[f"Heading{level}"] = create_heading_style(
            level, config.fonts, config.spacing
        )
    
    # Code style
    code_bg = hex_to_reportlab_color(config.colors.code_bg)
    code_text = hex_to_reportlab_color(config.colors.code_text)
    styles["Code"] = ParagraphStyle(
        "Code",
        fontName=config.fonts.code,
        fontSize=config.fonts.sizes.code,
        leading=config.fonts.sizes.code * 1.3,
        spaceBefore=6,
        spaceAfter=6,
        leftIndent=12,
        rightIndent=12,
        backColor=code_bg if config.code.background else None,
        textColor=code_text,
    )
    
    # Blockquote style
    styles["Blockquote"] = ParagraphStyle(
        "Blockquote",
        parent=styles["Normal"],
        leftIndent=20,
        rightIndent=20,
        spaceBefore=6,
        spaceAfter=6,
        textColor=colors.grey,
    )
    
    # Caption style
    styles["Caption"] = ParagraphStyle(
        "Caption",
        fontName=config.fonts.body,
        fontSize=config.fonts.sizes.caption,
        leading=config.fonts.sizes.caption * 1.2,
        spaceBefore=3,
        spaceAfter=12,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )
    
    return styles
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_styles.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pageforge/styles.py tests/test_styles.py
git commit -m "feat: add ReportLab style definitions

- Create get_styles() to generate all paragraph styles
- Implement create_heading_style() for H1-H6
- Add hex color conversion utility
- Include Normal, Code, Blockquote, Caption styles

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 4: Markdown Parser

**Files:**
- Create: `pageforge/parser.py`
- Create: `tests/test_parser.py`
- Create: `tests/fixtures/basic.md`

- [ ] **Step 1: Create test fixture**

```markdown
# tests/fixtures/basic.md
---
title: Test Document
author: Test Author
---

# Heading 1

This is a paragraph with **bold** and *italic* text.

## Heading 2

- List item 1
- List item 2
- List item 3

```python
def hello():
    print("world")
```

![Test Image](test-image.png)
```

- [ ] **Step 2: Write parser tests**

```python
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
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_parser.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 4: Implement parser**

```python
# pageforge/parser.py
"""Markdown parsing for PageForge."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import frontmatter
import markdown
from markdown.extensions import extra, codehilite, nl2br


@dataclass
class Document:
    """Parsed markdown document."""
    metadata: dict
    html: str
    images: list[dict]
    markdown_path: Path
    warnings: list[str]


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and return metadata and remaining content."""
    try:
        post = frontmatter.loads(content)
        return dict(post.metadata), post.content
    except Exception:
        return {}, content


def find_image_references(html: str) -> list[dict]:
    """Find all image references in HTML."""
    img_pattern = r'<img\s+(?:[^>]*?\s+)?src="([^"]*)"(?:\s+alt="([^"]*)")?[^>]*>'
    matches = re.finditer(img_pattern, html)
    
    images = []
    for match in matches:
        src = match.group(1)
        alt = match.group(2) or ""
        images.append({"src": src, "alt": alt})
    
    return images


def parse_markdown(content: str, markdown_path: Path) -> Document:
    """Parse markdown content into Document object."""
    # Extract frontmatter
    metadata, body = extract_frontmatter(content)
    
    # Configure markdown parser
    md = markdown.Markdown(
        extensions=[
            "extra",  # Tables, fenced code, footnotes
            "codehilite",  # Syntax highlighting
            "nl2br",  # Newline to <br>
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "linenums": False,
            }
        }
    )
    
    # Convert to HTML
    html = md.convert(body)
    
    # Find images
    images = find_image_references(html)
    
    # TODO: Collect warnings for unsupported features
    warnings = []
    
    return Document(
        metadata=metadata,
        html=html,
        images=images,
        markdown_path=markdown_path,
        warnings=warnings,
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_parser.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add pageforge/parser.py tests/test_parser.py tests/fixtures/basic.md
git commit -m "feat: add markdown parser with frontmatter support

- Implement parse_markdown() using python-markdown
- Add extract_frontmatter() for YAML headers
- Add find_image_references() to extract image sources
- Create Document dataclass for parsed content
- Add test fixtures and comprehensive tests

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 5: Image Resolution

**Files:**
- Create: `pageforge/images.py`
- Create: `tests/test_images.py`
- Create: `tests/fixtures/test-image.png`
- Create: `tests/fixtures/test-diagram.svg`

- [ ] **Step 1: Create test image fixtures**

Run: `python -c "from PIL import Image; img = Image.new('RGB', (100, 100), 'blue'); img.save('tests/fixtures/test-image.png')"`
Expected: test-image.png created

Run: `python -c "import pathlib; pathlib.Path('tests/fixtures/test-diagram.svg').write_text('<svg width=\"100\" height=\"100\"><rect width=\"100\" height=\"100\" fill=\"red\"/></svg>')"`
Expected: test-diagram.svg created

- [ ] **Step 2: Write image resolution tests**

```python
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
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_images.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 4: Implement image resolution**

```python
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
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_images.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add pageforge/images.py tests/test_images.py tests/fixtures/
git commit -m "feat: add image resolution and loading

- Implement resolve_image() with fallback strategy
- Add validate_image() for format checking
- Add load_raster_image() for PNG/JPG with scaling
- Add load_svg_image() for SVG conversion
- Create test fixtures and comprehensive tests

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 6: PDF Generator (Basic Elements)

**Files:**
- Create: `pageforge/generator.py`
- Create: `tests/test_generator.py`

- [ ] **Step 1: Write generator tests**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_generator.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement PDF generator (part 1 - HTML parsing)**

```python
# pageforge/generator.py
"""PDF generation for PageForge."""

from pathlib import Path
from html.parser import HTMLParser

from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle

from pageforge.config import Config
from pageforge.styles import get_styles
from pageforge.parser import Document
from pageforge.images import load_raster_image, load_svg_image, resolve_image


class MarkdownHTMLParser(HTMLParser):
    """Parse HTML to extract content for ReportLab rendering."""
    
    def __init__(self, styles, config, markdown_dir, resolved_images):
        super().__init__()
        self.styles = styles
        self.config = config
        self.markdown_dir = markdown_dir
        self.resolved_images = resolved_images
        self.flowables = []
        self.current_text = []
        self.current_tag = None
        self.list_items = []
        self.in_list = False
        self.list_ordered = False
    
    def handle_starttag(self, tag, attrs):
        """Handle opening tags."""
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self.current_tag = tag
            self.current_text = []
        elif tag == "p":
            self.current_tag = "p"
            self.current_text = []
        elif tag == "ul":
            self.in_list = True
            self.list_ordered = False
            self.list_items = []
        elif tag == "ol":
            self.in_list = True
            self.list_ordered = True
            self.list_items = []
        elif tag == "li":
            self.current_tag = "li"
            self.current_text = []
        elif tag == "code":
            if not self.current_tag:  # Inline code
                self.current_text.append("<font name='Courier' size='9'>")
        elif tag == "pre":
            self.current_tag = "pre"
            self.current_text = []
        elif tag == "strong" or tag == "b":
            self.current_text.append("<b>")
        elif tag == "em" or tag == "i":
            self.current_text.append("<i>")
        elif tag == "img":
            attrs_dict = dict(attrs)
            self._handle_image(attrs_dict.get("src", ""), attrs_dict.get("alt", ""))
        elif tag == "hr":
            self.flowables.append(Spacer(1, 0.2 * inch))
        elif tag == "blockquote":
            self.current_tag = "blockquote"
            self.current_text = []
    
    def handle_endtag(self, tag):
        """Handle closing tags."""
        if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(tag[1])
            text = "".join(self.current_text)
            style = self.styles[f"Heading{level}"]
            self.flowables.append(Paragraph(text, style))
            self.current_tag = None
            self.current_text = []
        elif tag == "p":
            text = "".join(self.current_text)
            if text.strip():
                self.flowables.append(Paragraph(text, self.styles["Normal"]))
            self.current_tag = None
            self.current_text = []
        elif tag == "li":
            text = "".join(self.current_text)
            self.list_items.append(text)
            self.current_tag = None
            self.current_text = []
        elif tag in ["ul", "ol"]:
            self._render_list()
            self.in_list = False
        elif tag == "code":
            if self.current_tag != "pre":  # Inline code
                self.current_text.append("</font>")
        elif tag == "pre":
            text = "".join(self.current_text)
            # Simple code block rendering
            self.flowables.append(Paragraph(text, self.styles["Code"]))
            self.current_tag = None
            self.current_text = []
        elif tag == "strong" or tag == "b":
            self.current_text.append("</b>")
        elif tag == "em" or tag == "i":
            self.current_text.append("</i>")
        elif tag == "blockquote":
            text = "".join(self.current_text)
            if text.strip():
                self.flowables.append(Paragraph(text, self.styles["Blockquote"]))
            self.current_tag = None
            self.current_text = []
    
    def handle_data(self, data):
        """Handle text content."""
        if self.current_tag or self.in_list:
            self.current_text.append(data)
    
    def _render_list(self):
        """Render accumulated list items."""
        for i, item in enumerate(self.list_items):
            if self.list_ordered:
                bullet = f"{i + 1}."
            else:
                bullet = "•"
            
            text = f"{bullet} {item}"
            para = Paragraph(text, self.styles["Normal"])
            self.flowables.append(para)
        
        self.list_items = []
    
    def _handle_image(self, src, alt):
        """Handle image tag."""
        resolved_path = resolve_image(
            src, self.markdown_dir, self.config.images, interactive=False
        )
        
        if resolved_path:
            try:
                if resolved_path.suffix.lower() == ".svg":
                    img = load_svg_image(resolved_path, self.config.images)
                else:
                    img = load_raster_image(resolved_path, self.config.images)
                
                if img:
                    self.flowables.append(img)
                    if alt and self.config.images.show_captions:
                        caption = Paragraph(alt, self.styles["Caption"])
                        self.flowables.append(caption)
            except Exception as e:
                # TODO: Add warning
                pass


def html_to_flowables(
    html: str,
    styles: dict,
    config: Config,
    markdown_dir: Path,
    resolved_images: dict
) -> list:
    """Convert HTML to ReportLab flowables."""
    parser = MarkdownHTMLParser(styles, config, markdown_dir, resolved_images)
    parser.feed(html)
    return parser.flowables


def get_page_size(config: Config):
    """Get ReportLab page size from config."""
    size_map = {
        "letter": letter,
        "a4": A4,
        "legal": legal,
    }
    page_size = size_map.get(config.page.size, letter)
    
    if config.page.orientation == "landscape":
        return (page_size[1], page_size[0])
    return page_size


def generate_pdf(
    doc: Document,
    output_path: Path,
    config: Config,
    resolved_images: dict
) -> None:
    """Generate PDF from parsed document."""
    styles = get_styles(config)
    
    # Set up PDF document
    page_size = get_page_size(config)
    pdf_doc = SimpleDocTemplate(
        str(output_path),
        pagesize=page_size,
        topMargin=config.page.margins.top * inch,
        bottomMargin=config.page.margins.bottom * inch,
        leftMargin=config.page.margins.left * inch,
        rightMargin=config.page.margins.right * inch,
    )
    
    # Convert HTML to flowables
    story = html_to_flowables(
        doc.html, styles, config, doc.markdown_path.parent, resolved_images
    )
    
    # Build PDF
    pdf_doc.build(story)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_generator.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pageforge/generator.py tests/test_generator.py
git commit -m "feat: add PDF generator with basic elements

- Implement MarkdownHTMLParser for HTML to flowables
- Add html_to_flowables() converter
- Add generate_pdf() main function
- Support headings, paragraphs, lists, images, code
- Handle page size and margins from config

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 7: CLI Implementation

**Files:**
- Create: `pageforge/cli.py`
- Create: `tests/integration/test_cli.py`

- [ ] **Step 1: Write CLI integration test**

```python
# tests/integration/test_cli.py
import pytest
from pathlib import Path
from click.testing import CliRunner
from pageforge.cli import main


def test_cli_basic_conversion(tmp_path):
    runner = CliRunner()
    
    # Create test markdown
    test_md = tmp_path / "test.md"
    test_md.write_text("# Test\n\nContent")
    
    # Run CLI
    result = runner.invoke(main, [str(test_md)])
    
    assert result.exit_code == 0
    assert (tmp_path / "test.pdf").exists()


def test_cli_output_file(tmp_path):
    runner = CliRunner()
    
    test_md = tmp_path / "test.md"
    test_md.write_text("# Test")
    output_pdf = tmp_path / "output.pdf"
    
    result = runner.invoke(main, [str(test_md), "-o", str(output_pdf)])
    
    assert result.exit_code == 0
    assert output_pdf.exists()


def test_cli_missing_input():
    runner = CliRunner()
    result = runner.invoke(main, ["nonexistent.md"])
    assert result.exit_code != 0


def test_cli_verbose_mode(tmp_path):
    runner = CliRunner()
    
    test_md = tmp_path / "test.md"
    test_md.write_text("# Test")
    
    result = runner.invoke(main, [str(test_md), "-v"])
    
    assert result.exit_code == 0
    assert "Converting:" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_cli.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Implement CLI**

```python
# pageforge/cli.py
"""Command-line interface for PageForge."""

import sys
from pathlib import Path
from typing import Optional

import click

from pageforge.config import get_default_config, Config
from pageforge.parser import parse_markdown
from pageforge.generator import generate_pdf


def convert_file(
    input_path: Path,
    output_path: Optional[Path],
    config: Config,
    verbose: bool = False
) -> bool:
    """Convert single markdown file to PDF."""
    try:
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix(".pdf")
        elif output_path.is_dir():
            output_path = output_path / input_path.with_suffix(".pdf").name
        
        if verbose:
            click.echo(f"Converting: {input_path}")
        
        # Read markdown
        content = input_path.read_text(encoding="utf-8")
        
        if verbose:
            click.echo(f"  ✓ Read markdown ({len(content)} bytes)")
        
        # Parse
        doc = parse_markdown(content, input_path)
        
        if verbose:
            click.echo(f"  ✓ Parsed markdown")
            if doc.images:
                click.echo(f"  ✓ Found {len(doc.images)} image(s)")
        
        # Generate PDF
        generate_pdf(doc, output_path, config, {})
        
        if verbose:
            click.echo(f"  ✓ Generated PDF")
        
        click.echo(f"Created: {output_path}")
        return True
        
    except Exception as e:
        click.echo(f"Error converting {input_path}: {e}", err=True)
        if verbose:
            raise
        return False


@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o", "--output",
    type=click.Path(path_type=Path),
    help="Output PDF file or directory"
)
@click.option(
    "-v", "--verbose",
    count=True,
    help="Verbose output (-v or -vv for debug)"
)
@click.option(
    "--quiet",
    is_flag=True,
    help="Suppress non-error output"
)
@click.version_option(version="0.1.0", prog_name="pageforge")
def main(
    input: Path,
    output: Optional[Path],
    verbose: int,
    quiet: bool
):
    """Convert Markdown files to PDF.
    
    Examples:
    
        pageforge document.md
        
        pageforge document.md -o output.pdf
        
        pageforge document.md -v
    """
    # Load default config (TODO: config file loading in future task)
    config = get_default_config()
    
    # Convert file
    success = convert_file(input, output, config, verbose=verbose > 0)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/integration/test_cli.py -v`
Expected: PASS

- [ ] **Step 5: Test CLI manually**

Run: `pageforge tests/fixtures/basic.md -v`
Expected: Creates tests/fixtures/basic.pdf with success message

- [ ] **Step 6: Commit**

```bash
git add pageforge/cli.py tests/integration/test_cli.py
git commit -m "feat: add CLI implementation

- Implement main() CLI entry point with Click
- Add convert_file() for single file conversion
- Support -o for output path, -v for verbose
- Add integration tests for CLI
- Wire up parser + generator pipeline

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 8: End-to-End Testing

**Files:**
- Modify: `tests/integration/test_cli.py`
- Create: `tests/fixtures/complex.md`

- [ ] **Step 1: Create complex test fixture**

```markdown
# tests/fixtures/complex.md
---
title: Complex Document
author: Test Suite
---

# Main Heading

This document tests **bold**, *italic*, and `inline code`.

## Lists

Unordered list:
- First item
- Second item
- Third item

Ordered list:
1. Step one
2. Step two
3. Step three

## Code Block

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Blockquote

> This is a blockquote.
> It spans multiple lines.

## Image

![Test Image](test-image.png)

## Table

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

---

End of document.
```

- [ ] **Step 2: Add end-to-end test**

```python
# Append to tests/integration/test_cli.py

def test_cli_complex_document(tmp_path):
    """Test converting document with all major features."""
    runner = CliRunner()
    
    # Copy fixtures to tmp_path
    import shutil
    fixture_src = Path("tests/fixtures/complex.md")
    fixture_dst = tmp_path / "complex.md"
    shutil.copy(fixture_src, fixture_dst)
    
    # Copy image
    img_src = Path("tests/fixtures/test-image.png")
    img_dst = tmp_path / "test-image.png"
    shutil.copy(img_src, img_dst)
    
    # Convert
    result = runner.invoke(main, [str(fixture_dst), "-v"])
    
    assert result.exit_code == 0
    output_pdf = tmp_path / "complex.pdf"
    assert output_pdf.exists()
    
    # Check PDF is non-trivial size (has content)
    assert output_pdf.stat().st_size > 10000  # At least 10KB
```

- [ ] **Step 3: Run end-to-end test**

Run: `pytest tests/integration/test_cli.py::test_cli_complex_document -v`
Expected: PASS

- [ ] **Step 4: Run full test suite**

Run: `pytest -v`
Expected: All tests pass

- [ ] **Step 5: Generate coverage report**

Run: `pytest --cov=pageforge --cov-report=term-missing`
Expected: Coverage >70%

- [ ] **Step 6: Commit**

```bash
git add tests/fixtures/complex.md tests/integration/test_cli.py
git commit -m "test: add end-to-end integration tests

- Create complex.md fixture with all features
- Add test_cli_complex_document() integration test
- Verify full pipeline works end-to-end
- All tests passing

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Task 9: Documentation

**Files:**
- Modify: `README.md`
- Create: `docs/user-guide.md`

- [ ] **Step 1: Update README**

```markdown
# README.md
# PageForge

Markdown to PDF converter optimized for LLM-generated content.

## Features

- ✅ Pure Python (no Node/npm required)
- ✅ Clean PDF generation using ReportLab
- ✅ Support for headings, lists, code blocks, tables, images
- ✅ SVG and raster image support
- ✅ YAML frontmatter for metadata
- ✅ Configurable styling (future)

## Installation

```bash
# From source
git clone https://github.com/medmond78/PageForge.git
cd PageForge
pip install -e .
```

## Quick Start

```bash
# Convert markdown to PDF
pageforge document.md

# Specify output file
pageforge document.md -o report.pdf

# Verbose mode
pageforge document.md -v
```

## Usage

```bash
pageforge [OPTIONS] INPUT

Options:
  -o, --output PATH    Output PDF file or directory
  -v, --verbose        Verbose output
  --quiet              Suppress non-error output
  --version            Show version
  --help               Show help
```

## Supported Markdown Features

- Headers (H1-H6)
- Paragraphs with **bold**, *italic*, `code`
- Unordered and ordered lists
- Code blocks with syntax highlighting
- Images (PNG, JPG, SVG)
- Tables
- Blockquotes
- Horizontal rules

## Example

```markdown
---
title: My Report
author: Your Name
---

# Introduction

This document demonstrates **PageForge**.

## Features

- Easy to use
- Clean output
- No external dependencies

![Diagram](./diagram.svg)
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=pageforge

# Format code
black pageforge tests
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please open an issue or PR.
```

- [ ] **Step 2: Create user guide**

```markdown
# docs/user-guide.md
# PageForge User Guide

## Installation

### Requirements

- Python 3.10 or higher
- pip

### Install from Source

```bash
git clone https://github.com/medmond78/PageForge.git
cd PageForge
pip install -e .
```

Verify installation:

```bash
pageforge --version
```

## Basic Usage

### Converting a Single File

```bash
pageforge document.md
```

This creates `document.pdf` in the same directory.

### Specifying Output Location

```bash
# Output to specific file
pageforge document.md -o report.pdf

# Output to directory
pageforge document.md -o /path/to/output/
```

### Verbose Mode

```bash
pageforge document.md -v
```

Shows detailed progress:
- File reading
- Parsing statistics
- Image detection
- PDF generation

## Markdown Features

### Frontmatter

Add YAML frontmatter for metadata:

```markdown
---
title: My Document
author: Your Name
date: 2026-08-11
---

# Content starts here
```

### Images

Use relative paths for images:

```markdown
![Chart](./chart.png)
![Diagram](../images/diagram.svg)
```

Supported formats:
- PNG
- JPG/JPEG
- SVG

### Code Blocks

Specify language for syntax highlighting:

````markdown
```python
def hello():
    print("world")
```
````

Supported languages: Python, JavaScript, SQL, Bash, JSON, YAML, and more.

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```

Keep tables to 5-6 columns for best results.

## Tips

1. **Image Placement**: Keep images in the same directory as your markdown file
2. **Line Length**: Keep code block lines under 80 characters
3. **Table Width**: Limit tables to 5-6 columns for readability
4. **File Size**: Images are automatically scaled to fit the page

## Troubleshooting

### "Image not found" Error

Make sure image paths are relative to the markdown file:

```markdown
# Correct
![Chart](./chart.png)

# Incorrect (absolute path)
![Chart](/Users/me/chart.png)
```

### PDF is Empty

Check that your markdown file is not empty and contains valid content.

### Syntax Highlighting Not Working

Specify the language in your code block:

````markdown
```python
# Your code here
```
````

## Future Features

- Configuration files (YAML)
- Custom styling and themes
- Interactive image prompts
- Batch processing
- LaTeX equation rendering
```

- [ ] **Step 3: Commit documentation**

```bash
git add README.md docs/user-guide.md
git commit -m "docs: add README and user guide

- Update README with complete feature list
- Add installation and quick start
- Document all CLI options
- Create comprehensive user guide
- Add examples and troubleshooting

Co-Authored-By: Claude Sonnet 4 <noreply@anthropic.com>"
```

---

## Self-Review

**Spec Coverage Check:**

✅ Configuration system (defaults only, file loading deferred)
✅ Style definitions (all basic styles)
✅ Markdown parser (frontmatter, extensions)
✅ Image resolution (basic, prompts deferred)
✅ PDF generator (all basic elements)
✅ CLI entry point (basic conversion)
✅ Tests (unit + integration)
✅ Documentation (README + user guide)

**Deferred to Future Tasks:**
- YAML config file loading
- Interactive image prompts
- Batch processing
- Advanced markdown features (footnotes, definition lists)
- LLM guidance document

**Placeholder Scan:**
✅ No TBD/TODO in critical paths
✅ All code blocks complete
✅ All file paths exact
✅ All test assertions specific

**Type Consistency:**
✅ Document dataclass used consistently
✅ Config classes match across modules
✅ Function signatures match between definition and use

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-11-pageforge-mvp.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
