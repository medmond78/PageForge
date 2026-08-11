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
