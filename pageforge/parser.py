# pageforge/parser.py
"""Markdown parsing for PageForge."""

import re
from dataclasses import dataclass
from pathlib import Path

import frontmatter
import markdown


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
    except (AttributeError, ValueError, TypeError):
        # Invalid frontmatter format, treat as plain markdown
        return {}, content


def find_image_references(html: str) -> list[dict]:
    """Find all image references in HTML."""
    # Find all img tags
    img_tags = re.finditer(r'<img\s+([^>]+)/?>', html)

    images = []
    for tag in img_tags:
        attrs = tag.group(1)
        # Extract src
        src_match = re.search(r'src="([^"]*)"', attrs)
        # Extract alt
        alt_match = re.search(r'alt="([^"]*)"', attrs)

        if src_match:
            src = src_match.group(1)
            alt = alt_match.group(1) if alt_match else ""
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
