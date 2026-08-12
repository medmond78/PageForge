# pageforge/generator.py
"""PDF generation from parsed markdown."""

from html.parser import HTMLParser
from pathlib import Path

from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage,
    ListFlowable,
    ListItem,
    Preformatted,
)
from reportlab.lib.styles import ParagraphStyle

from pageforge.config import Config
from pageforge.parser import Document
from pageforge.images import resolve_image


class MarkdownHTMLParser(HTMLParser):
    """HTML parser that converts to ReportLab flowables.

    Limitations:
    - Nested lists are not supported. Inner and outer list items will be mixed
      into a single flat list. This is due to the use of single list_items and
      list_type variables instead of a stack-based approach.
    """

    def __init__(self, styles: dict, config: Config, markdown_dir: Path, image_cache: dict, interactive: bool = True):
        super().__init__()
        self.styles = styles
        self.config = config
        self.markdown_dir = markdown_dir
        self.image_cache = image_cache
        self.interactive = interactive
        self.missing_images = 0
        self.flowables = []
        self.current_tag = None
        self.tag_stack = []
        self.data_buffer = []
        self.list_items = []
        self.list_type = None  # 'ul' or 'ol'
        self.in_code_block = False
        self.code_buffer = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Handle opening HTML tags."""
        self.tag_stack.append(tag)

        if tag in ['ul', 'ol']:
            self.list_type = tag
            self.list_items = []
        elif tag == 'li':
            self.data_buffer = []
        elif tag == 'pre':
            self.in_code_block = True
            self.code_buffer = []
        elif tag == 'code' and not self.in_code_block:
            self.data_buffer.append('<font name="Courier">')
        elif tag == 'strong' or tag == 'b':
            self.data_buffer.append('<b>')
        elif tag == 'em' or tag == 'i':
            self.data_buffer.append('<i>')
        elif tag == 'img':
            self._handle_image(attrs)
        elif tag == 'hr':
            self.flowables.append(Spacer(1, 12))
            self.flowables.append(Paragraph('<hr/>', self.styles['Normal']))
            self.flowables.append(Spacer(1, 12))
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.current_tag = tag
            self.data_buffer = []
        elif tag == 'p':
            self.current_tag = 'p'
            self.data_buffer = []
        elif tag == 'blockquote':
            self.current_tag = 'blockquote'
            self.data_buffer = []

    def handle_endtag(self, tag: str) -> None:
        """Handle closing HTML tags."""
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = ''.join(self.data_buffer).strip()
            if text:
                level = int(tag[1])
                style = self.styles.get(f'Heading{level}', self.styles['Normal'])
                self.flowables.append(Paragraph(text, style))
            self.data_buffer = []
            self.current_tag = None
        elif tag == 'p':
            text = ''.join(self.data_buffer).strip()
            if text:
                self.flowables.append(Paragraph(text, self.styles['Normal']))
            self.data_buffer = []
            self.current_tag = None
        elif tag == 'blockquote':
            text = ''.join(self.data_buffer).strip()
            if text:
                self.flowables.append(Paragraph(text, self.styles['Blockquote']))
            self.data_buffer = []
            self.current_tag = None
        elif tag == 'li':
            text = ''.join(self.data_buffer).strip()
            if text:
                self.list_items.append(text)
            self.data_buffer = []
        elif tag in ['ul', 'ol']:
            if self.list_items:
                # Create list flowable
                bullet_type = 'bullet' if tag == 'ul' else 'decimal'
                list_items = []
                for item_text in self.list_items:
                    para = Paragraph(item_text, self.styles['Normal'])
                    list_items.append(ListItem(para, leftIndent=self.config.spacing.list_indent))

                list_flowable = ListFlowable(
                    list_items,
                    bulletType=bullet_type,
                    start=1 if tag == 'ol' else None,
                )
                self.flowables.append(list_flowable)

            self.list_items = []
            self.list_type = None
        elif tag == 'pre':
            code_text = ''.join(self.code_buffer)
            if code_text:
                self.flowables.append(Preformatted(code_text, self.styles['Code']))
            self.in_code_block = False
            self.code_buffer = []
        elif tag == 'code' and not self.in_code_block:
            self.data_buffer.append('</font>')
        elif tag == 'strong' or tag == 'b':
            self.data_buffer.append('</b>')
        elif tag == 'em' or tag == 'i':
            self.data_buffer.append('</i>')

    def handle_data(self, data: str) -> None:
        """Handle text data between tags."""
        if self.in_code_block:
            self.code_buffer.append(data)
        else:
            self.data_buffer.append(data)

    def _handle_image(self, attrs: list[tuple[str, str | None]]) -> None:
        """Handle image tags."""
        attrs_dict = dict(attrs)
        src = attrs_dict.get('src', '')
        alt = attrs_dict.get('alt', '')

        if not src:
            return

        # Resolve image path
        resolved_path = resolve_image(
            src,
            self.markdown_dir,
            self.config.images,
            interactive=self.interactive
        )

        if resolved_path is None or not resolved_path.exists():
            # Track missing image
            self.missing_images += 1
            # Add warning paragraph
            warning_text = f"[Image not found: {src}]"
            self.flowables.append(Paragraph(warning_text, self.styles['Normal']))
            return

        # Check cache
        if str(resolved_path) in self.image_cache:
            img_flowable = self.image_cache[str(resolved_path)]
            self.flowables.append(img_flowable)
        else:
            # Create image flowable
            try:
                max_width = self.config.images.max_width * inch
                max_height = self.config.images.max_height * inch

                img = RLImage(str(resolved_path))

                # Validate image dimensions to prevent division by zero
                if img.imageWidth <= 0 or img.imageHeight <= 0:
                    warning_text = f"[Image has invalid dimensions: {src}]"
                    self.flowables.append(Paragraph(warning_text, self.styles['Normal']))
                    return

                # Scale to fit
                aspect = img.imageHeight / img.imageWidth
                if img.imageWidth > max_width:
                    img.drawWidth = max_width
                    img.drawHeight = max_width * aspect
                if img.drawHeight > max_height:
                    img.drawHeight = max_height
                    img.drawWidth = max_height / aspect

                self.image_cache[str(resolved_path)] = img
                self.flowables.append(img)

                # Add caption if configured
                if self.config.images.show_captions and alt:
                    self.flowables.append(Paragraph(alt, self.styles['Caption']))

            except (IOError, OSError, ValueError) as e:
                # Image load failed
                warning_text = f"[Image load error: {src}]"
                self.flowables.append(Paragraph(warning_text, self.styles['Normal']))


def html_to_flowables(
    html: str,
    styles: dict,
    config: Config,
    markdown_dir: Path,
    image_cache: dict,
    interactive: bool = True
) -> tuple[list, int]:
    """Convert HTML to ReportLab flowables.

    Returns:
        Tuple of (flowables list, missing_images count)
    """
    parser = MarkdownHTMLParser(styles, config, markdown_dir, image_cache, interactive)
    parser.feed(html)
    return parser.flowables, parser.missing_images


def get_page_size(size_name: str, orientation: str) -> tuple[float, float]:
    """Get page size from name and orientation."""
    size_map = {
        'letter': letter,
        'a4': A4,
        'legal': legal,
    }

    size = size_map.get(size_name.lower(), letter)

    if orientation.lower() == 'landscape':
        return size[1], size[0]
    else:
        return size


def generate_pdf(
    doc: Document,
    output_path: Path,
    config: Config,
    image_cache: dict,
    interactive: bool = True
) -> int:
    """Generate PDF from parsed document.

    Returns:
        Number of missing images
    """
    from pageforge.styles import get_styles

    # Get styles
    styles = get_styles(config)

    # Convert HTML to flowables
    flowables, missing_count = html_to_flowables(
        doc.html,
        styles,
        config,
        doc.markdown_path.parent,
        image_cache,
        interactive
    )

    # Create PDF document
    page_size = get_page_size(config.page.size, config.page.orientation)

    pdf_doc = SimpleDocTemplate(
        str(output_path),
        pagesize=page_size,
        topMargin=config.page.margins.top * inch,
        bottomMargin=config.page.margins.bottom * inch,
        leftMargin=config.page.margins.left * inch,
        rightMargin=config.page.margins.right * inch,
    )

    # Build PDF
    pdf_doc.build(flowables)

    return missing_count
