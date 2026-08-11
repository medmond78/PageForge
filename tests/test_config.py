# tests/test_config.py
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


def test_color_config_defaults():
    from pageforge.config import ColorConfig
    colors = ColorConfig()
    assert colors.text == "#000000"
    assert colors.headings == "#1a1a1a"
    assert colors.code_bg == "#f5f5f5"
    assert colors.code_text == "#2c3e50"
    assert colors.links == "#0066cc"
    assert colors.table_header == "#e8e8e8"


def test_spacing_config_defaults():
    from pageforge.config import SpacingConfig
    spacing = SpacingConfig()
    assert spacing.paragraph == 12
    assert spacing.heading_before == 18
    assert spacing.heading_after == 6
    assert spacing.line_height == 1.2
    assert spacing.list_indent == 20


def test_image_config_defaults():
    from pageforge.config import ImageConfig
    images = ImageConfig()
    assert images.max_width == 6.5
    assert images.max_height == 9.0
    assert images.dpi == 150
    assert images.fallback_dir is None
    assert images.center_align is True
    assert images.show_captions is True


def test_code_config_defaults():
    from pageforge.config import CodeConfig
    code = CodeConfig()
    assert code.syntax_highlight is True
    assert code.theme == "default"
    assert code.show_line_numbers is False
    assert code.wrap_long_lines is True
    assert code.background is True


def test_font_sizes_defaults():
    from pageforge.config import FontSizes
    sizes = FontSizes()
    assert sizes.h1 == 24
    assert sizes.h2 == 18
    assert sizes.h3 == 14
    assert sizes.h4 == 12
    assert sizes.h5 == 11
    assert sizes.h6 == 10
    assert sizes.body == 11
    assert sizes.code == 9
    assert sizes.caption == 9
