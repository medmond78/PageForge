# pageforge/cli.py
"""Command-line interface for PageForge."""

import sys
from pathlib import Path
from typing import Optional

import click
import yaml

from pageforge.config import Config, get_default_config
from pageforge.parser import parse_markdown
from pageforge.generator import generate_pdf


def load_config_from_yaml(config_path: Path) -> Config:
    """Load configuration from YAML file and merge with defaults.

    Args:
        config_path: Path to YAML config file

    Returns:
        Config object with merged settings

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML is invalid
        ValueError: If config values are invalid
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    # Load YAML
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    if config_data is None:
        config_data = {}

    # Start with defaults
    config = get_default_config()

    # Merge YAML data into config
    # This is a simple deep merge for nested dictionaries
    if 'page' in config_data:
        page = config_data['page']
        if 'size' in page:
            config.page.size = page['size']
        if 'orientation' in page:
            config.page.orientation = page['orientation']
        if 'margins' in page:
            margins = page['margins']
            if 'top' in margins:
                config.page.margins.top = float(margins['top'])
            if 'bottom' in margins:
                config.page.margins.bottom = float(margins['bottom'])
            if 'left' in margins:
                config.page.margins.left = float(margins['left'])
            if 'right' in margins:
                config.page.margins.right = float(margins['right'])

    if 'fonts' in config_data:
        fonts = config_data['fonts']
        if 'body' in fonts:
            config.fonts.body = fonts['body']
        if 'heading' in fonts:
            config.fonts.heading = fonts['heading']
        if 'code' in fonts:
            config.fonts.code = fonts['code']
        if 'sizes' in fonts:
            sizes = fonts['sizes']
            if 'h1' in sizes:
                config.fonts.sizes.h1 = int(sizes['h1'])
            if 'h2' in sizes:
                config.fonts.sizes.h2 = int(sizes['h2'])
            if 'h3' in sizes:
                config.fonts.sizes.h3 = int(sizes['h3'])
            if 'h4' in sizes:
                config.fonts.sizes.h4 = int(sizes['h4'])
            if 'h5' in sizes:
                config.fonts.sizes.h5 = int(sizes['h5'])
            if 'h6' in sizes:
                config.fonts.sizes.h6 = int(sizes['h6'])
            if 'body' in sizes:
                config.fonts.sizes.body = int(sizes['body'])
            if 'code' in sizes:
                config.fonts.sizes.code = int(sizes['code'])
            if 'caption' in sizes:
                config.fonts.sizes.caption = int(sizes['caption'])

    if 'colors' in config_data:
        colors = config_data['colors']
        if 'text' in colors:
            config.colors.text = colors['text']
        if 'headings' in colors:
            config.colors.headings = colors['headings']
        if 'code_bg' in colors:
            config.colors.code_bg = colors['code_bg']
        if 'code_text' in colors:
            config.colors.code_text = colors['code_text']
        if 'links' in colors:
            config.colors.links = colors['links']
        if 'table_header' in colors:
            config.colors.table_header = colors['table_header']

    if 'spacing' in config_data:
        spacing = config_data['spacing']
        if 'paragraph' in spacing:
            config.spacing.paragraph = int(spacing['paragraph'])
        if 'heading_before' in spacing:
            config.spacing.heading_before = int(spacing['heading_before'])
        if 'heading_after' in spacing:
            config.spacing.heading_after = int(spacing['heading_after'])
        if 'line_height' in spacing:
            config.spacing.line_height = float(spacing['line_height'])
        if 'list_indent' in spacing:
            config.spacing.list_indent = int(spacing['list_indent'])

    if 'images' in config_data:
        images = config_data['images']
        if 'max_width' in images:
            config.images.max_width = float(images['max_width'])
        if 'max_height' in images:
            config.images.max_height = float(images['max_height'])
        if 'dpi' in images:
            config.images.dpi = int(images['dpi'])
        if 'fallback_dir' in images:
            config.images.fallback_dir = images['fallback_dir']
        if 'center_align' in images:
            config.images.center_align = bool(images['center_align'])
        if 'show_captions' in images:
            config.images.show_captions = bool(images['show_captions'])

    if 'code' in config_data:
        code = config_data['code']
        if 'syntax_highlight' in code:
            config.code.syntax_highlight = bool(code['syntax_highlight'])
        if 'theme' in code:
            config.code.theme = code['theme']
        if 'show_line_numbers' in code:
            config.code.show_line_numbers = bool(code['show_line_numbers'])
        if 'wrap_long_lines' in code:
            config.code.wrap_long_lines = bool(code['wrap_long_lines'])
        if 'background' in code:
            config.code.background = bool(code['background'])

    return config


def convert_file(markdown_path: Path, output_path: Path, config: Config, interactive: bool = True) -> dict:
    """Convert a markdown file to PDF.

    Args:
        markdown_path: Path to input markdown file
        output_path: Path to output PDF file
        config: Configuration object
        interactive: Enable interactive prompts for missing images

    Returns:
        Dictionary with 'missing_images' count

    Raises:
        FileNotFoundError: If markdown file doesn't exist
        IsADirectoryError: If markdown_path is a directory
        ValueError: If file cannot be processed
        IOError: If file cannot be read or written
    """
    # Validate input
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    if markdown_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: {markdown_path}")

    # Read markdown file
    try:
        content = markdown_path.read_text(encoding='utf-8')
    except Exception as e:
        raise IOError(f"Failed to read markdown file: {e}") from e

    # Parse markdown
    doc = parse_markdown(content, markdown_path)

    # Generate PDF with image cache
    image_cache = {}
    result = {'missing_images': 0}
    try:
        missing_count = generate_pdf(doc, output_path, config, image_cache, interactive)
        result['missing_images'] = missing_count
    except Exception as e:
        raise ValueError(f"Failed to generate PDF: {e}") from e

    return result


@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument('output_file', required=False, type=click.Path(path_type=Path))
@click.option(
    '--config',
    'config_path',
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help='Path to YAML configuration file'
)
@click.option(
    '--no-prompt',
    '-n',
    is_flag=True,
    help='Disable interactive prompts for missing images. Exit with code 2 if any images are missing.'
)
def main(input_file: Path, output_file: Optional[Path], config_path: Optional[Path], no_prompt: bool) -> None:
    """Convert Markdown to PDF.

    INPUT_FILE: Path to markdown file to convert

    OUTPUT_FILE: Path to output PDF file (optional, defaults to <input-name>.pdf)
    """
    # Determine output path
    if output_file is None:
        output_file = input_file.with_suffix('.pdf')

    # Determine interactive mode
    interactive = not no_prompt

    # Load configuration
    try:
        if config_path:
            config = load_config_from_yaml(config_path)
        else:
            config = get_default_config()
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except yaml.YAMLError as e:
        click.echo(f"Error: Invalid YAML in config file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: Failed to load config: {e}", err=True)
        sys.exit(1)

    # Convert file
    try:
        result = convert_file(input_file, output_file, config, interactive)
        click.echo(f"PDF generated: {output_file}")

        # Exit with code 2 if images are missing in non-interactive mode
        if not interactive and result['missing_images'] > 0:
            click.echo(f"Warning: {result['missing_images']} image(s) not found", err=True)
            sys.exit(2)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except (IsADirectoryError, ValueError, IOError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: Unexpected error during conversion: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
