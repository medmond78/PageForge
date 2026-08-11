# pageforge/styles.py
"""ReportLab style definitions for PageForge."""

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

from pageforge.config import Config, FontConfig, SpacingConfig


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
    spacing: SpacingConfig,
    heading_color: colors.Color
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
        textColor=heading_color,
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
    heading_color = hex_to_reportlab_color(config.colors.headings)
    for level in range(1, 7):
        styles[f"Heading{level}"] = create_heading_style(
            level, config.fonts, config.spacing, heading_color
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
