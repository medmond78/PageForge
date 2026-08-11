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
