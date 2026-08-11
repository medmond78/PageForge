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
