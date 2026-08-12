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
