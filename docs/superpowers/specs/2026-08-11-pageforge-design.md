# PageForge: Markdown to PDF Converter - Design Specification

**Created:** 2026-08-11  
**Author:** Matthew Pausley  
**Purpose:** Python-based CLI tool for converting Markdown documents to PDF, optimized for LLM-generated content

---

## 1. Project Overview

### 1.1 Goals

PageForge converts Markdown files to professional-looking PDFs with minimal external dependencies. The tool is designed to:

- Work reliably on IT-managed Windows machines without requiring Node/npm
- Handle LLM-generated markdown documents with embedded images
- Provide intuitive configuration for casual users
- Be callable from Claude Code via simple CLI commands
- Include comprehensive guidance for LLM agents generating markdown

### 1.2 Non-Goals (Initial Release)

- LaTeX document generation (future enhancement)
- Interactive HTML output
- Real-time preview/watch mode
- GUI interface
- Cloud-based conversion

### 1.3 Target Use Cases

1. Converting LLM-generated summaries and synthesis documents to PDF
2. Creating reports from markdown with charts/diagrams (SVG/PNG)
3. Batch processing multiple markdown files
4. Automated document generation in Claude Code workflows

---

## 2. Technical Architecture

### 2.1 Core Technology Stack

**Primary approach:** Pure Python solution using ReportLab for PDF generation

**Why ReportLab over alternatives:**
- **No external binaries required** (vs Pandoc which needs LaTeX)
- **No system library dependencies** (vs WeasyPrint which needs Cairo/Pango on Windows)
- **Mature and stable** with excellent documentation
- **Pip-installable** without IT approval complications
- **Full control** over PDF rendering and styling

**Key Dependencies:**
- `reportlab` - PDF generation engine
- `markdown` - Markdown parsing with extensions
- `python-frontmatter` - YAML frontmatter extraction
- `Pillow` - PNG/JPG image handling
- `svglib` - SVG to ReportLab conversion
- `Pygments` - Syntax highlighting for code blocks
- `PyYAML` - Configuration file parsing
- `click` - CLI framework

### 2.2 Project Structure

```
pageforge/
├── pageforge/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point and argument parsing
│   ├── parser.py           # Markdown parsing and AST generation
│   ├── images.py           # Image resolution and conversion
│   ├── generator.py        # PDF generation with ReportLab
│   ├── config.py           # Configuration management
│   ├── styles.py           # Style definitions and themes
│   └── utils.py            # Shared utilities
├── tests/
│   ├── test_parser.py
│   ├── test_images.py
│   ├── test_generator.py
│   ├── fixtures/           # Test markdown files and images
│   └── integration/        # End-to-end tests
├── docs/
│   ├── llm-markdown-guide.md    # Guidance for LLM-generated content
│   ├── configuration.md         # Detailed config documentation
│   ├── user-guide.md           # End-user documentation
│   └── superpowers/
│       └── specs/              # Design specifications
├── examples/
│   ├── basic-report.md
│   ├── technical-doc.md
│   ├── pageforge.yaml          # Example configuration
│   └── assets/                 # Example images
├── pyproject.toml              # Project metadata and dependencies
├── README.md
├── LICENSE
└── .gitignore
```

### 2.3 Component Details

#### 2.3.1 CLI Module (`cli.py`)

**Responsibilities:**
- Parse command-line arguments
- Discover and load configuration
- Orchestrate conversion pipeline
- Handle user interactions (missing images)
- Provide helpful error messages

**Key Functions:**
```python
def main() -> int:
    """Main entry point for pageforge CLI"""

def convert_file(input_path, output_path, config) -> bool:
    """Convert single markdown file to PDF"""

def convert_batch(input_paths, output_dir, config) -> dict:
    """Convert multiple markdown files"""

def init_config(output_path) -> None:
    """Generate annotated config template"""

def show_config(config_path=None) -> None:
    """Display active configuration"""
```

**CLI Commands:**
```bash
# Basic conversion
pageforge document.md
pageforge document.md -o output.pdf
pageforge document.md -o /output/dir/

# Configuration
pageforge --init-config
pageforge --show-config
pageforge document.md --config custom.yaml

# Batch processing
pageforge *.md
pageforge directory/

# Image handling
pageforge document.md --image-dir ./assets
pageforge document.md --no-prompt

# Output control
pageforge document.md -v           # Verbose
pageforge document.md -vv          # Debug
pageforge document.md --quiet      # Quiet mode
```

**Exit Codes:**
- `0` - Success
- `1` - Conversion failed (invalid markdown, parsing error)
- `2` - Missing images with `--no-prompt` flag
- `3` - Invalid configuration file

#### 2.3.2 Parser Module (`parser.py`)

**Responsibilities:**
- Parse markdown using Python `markdown` library
- Extract YAML frontmatter (if present)
- Identify and validate image references
- Generate document structure suitable for PDF rendering
- Handle markdown extensions (tables, fenced code, etc.)

**Markdown Extensions Used:**
- `extra` - Tables, fenced code blocks, footnotes
- `codehilite` - Code syntax highlighting
- `toc` - Table of contents generation
- `meta` - Metadata extraction
- `nl2br` - Newline to break conversion

**Key Functions:**
```python
def parse_markdown(content: str) -> Document:
    """Parse markdown string into Document object"""

def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and remaining content"""

def find_images(ast: MarkdownAST) -> list[ImageReference]:
    """Find all image references in parsed markdown"""

def validate_markdown(content: str) -> list[ValidationWarning]:
    """Check for common issues (unsupported features, etc.)"""
```

**Document Structure:**
```python
@dataclass
class Document:
    metadata: dict              # From frontmatter
    content: MarkdownAST        # Parsed markdown tree
    images: list[ImageReference]
    warnings: list[str]         # Conversion warnings
```

#### 2.3.3 Image Resolver (`images.py`)

**Responsibilities:**
- Resolve relative image paths
- Fall back to configured directories
- Prompt user for missing images (interactive mode)
- Convert SVG to ReportLab-compatible format
- Load and validate raster images (PNG/JPG)
- Cache resolved paths within session

**Resolution Strategy:**
1. Check path relative to markdown file directory
2. Check configured fallback directory (if set)
3. Prompt user for path (if interactive)
4. Skip image or abort conversion

**Key Functions:**
```python
def resolve_image(
    image_ref: str,
    markdown_dir: Path,
    config: Config,
    interactive: bool = True
) -> Path | None:
    """Resolve image path with fallback and user prompting"""

def load_svg(path: Path) -> ReportLabDrawing:
    """Load SVG and convert to ReportLab drawing"""

def load_raster(path: Path, max_width: float, dpi: int) -> ReportLabImage:
    """Load PNG/JPG with size constraints"""

def validate_image(path: Path) -> bool:
    """Check if image is readable and supported format"""
```

**Image Prompt Format:**
```
Warning: Image not found: diagram.svg
  Referenced in: document.md line 42

Search locations checked:
  1. /path/to/document/diagram.svg (relative to markdown)
  2. /path/to/fallback/diagram.svg (from config)

Enter image path (or 'skip' to omit, 'abort' to cancel): _
```

#### 2.3.4 PDF Generator (`generator.py`)

**Responsibilities:**
- Create PDF using ReportLab
- Apply styling from configuration
- Render markdown elements (headings, paragraphs, lists, tables, code, images)
- Handle page layout, headers/footers
- Generate table of contents (if requested)

**Key Functions:**
```python
def generate_pdf(
    doc: Document,
    output_path: Path,
    config: Config,
    resolved_images: dict[str, Path]
) -> None:
    """Generate PDF from parsed document"""

def render_paragraph(text: str, style: ParagraphStyle) -> Flowable:
    """Render paragraph with inline formatting"""

def render_heading(text: str, level: int, style: ParagraphStyle) -> Flowable:
    """Render heading with appropriate styling"""

def render_code_block(code: str, language: str, style: CodeStyle) -> Flowable:
    """Render code block with syntax highlighting"""

def render_table(rows: list[list[str]], style: TableStyle) -> Flowable:
    """Render markdown table"""

def render_image(path: Path, caption: str, config: ImageConfig) -> Flowable:
    """Render image with caption"""

def render_list(items: list, ordered: bool, style: ListStyle) -> Flowable:
    """Render ordered or unordered list"""
```

**Rendering Strategy:**
- Use ReportLab's Platypus (Page Layout and Typography Using Scripts) framework
- Build document as sequence of Flowables (paragraphs, images, tables, etc.)
- Apply styles defined in configuration
- Handle page breaks automatically
- Support multi-column layouts (future enhancement)

#### 2.3.5 Configuration Manager (`config.py`)

**Responsibilities:**
- Load configuration from YAML files
- Merge user config with defaults
- Validate configuration values
- Provide config schema for documentation

**Configuration Discovery Order:**
1. Command-line `--config` argument
2. `pageforge.yaml` in current directory
3. `.pageforge.yaml` in user home directory
4. Built-in defaults

**Key Functions:**
```python
def load_config(config_path: Path = None) -> Config:
    """Load and merge configuration from multiple sources"""

def get_default_config() -> Config:
    """Return built-in default configuration"""

def validate_config(config: dict) -> list[ValidationError]:
    """Validate configuration schema and values"""

def merge_configs(base: dict, override: dict) -> dict:
    """Deep merge two configuration dictionaries"""
```

**Configuration Schema:**
```python
@dataclass
class Config:
    page: PageConfig
    fonts: FontConfig
    colors: ColorConfig
    spacing: SpacingConfig
    images: ImageConfig
    code: CodeConfig

@dataclass
class PageConfig:
    size: str = "letter"  # letter, a4, legal
    orientation: str = "portrait"  # portrait, landscape
    margins: Margins = field(default_factory=lambda: Margins(1.0, 1.0, 1.0, 1.0))

@dataclass
class FontConfig:
    body: str = "Helvetica"
    heading: str = "Helvetica-Bold"
    code: str = "Courier"
    sizes: FontSizes = field(default_factory=FontSizes)

# ... additional config classes
```

#### 2.3.6 Style Templates (`styles.py`)

**Responsibilities:**
- Define ReportLab ParagraphStyle objects for different elements
- Apply configuration to styles
- Provide theme presets

**Key Functions:**
```python
def get_styles(config: Config) -> StyleSheet:
    """Generate ReportLab styles from configuration"""

def create_heading_style(level: int, config: FontConfig) -> ParagraphStyle:
    """Create style for heading level"""

def create_code_style(config: CodeConfig) -> ParagraphStyle:
    """Create style for code blocks"""

def create_table_style(config: Config) -> TableStyle:
    """Create table formatting style"""
```

---

## 3. Configuration System

### 3.1 Default Configuration

The tool works out-of-the-box with no configuration required. Default settings optimized for readability.

### 3.2 Configuration File Format

**Example `pageforge.yaml` with extensive inline documentation:**

```yaml
# PageForge Configuration File
# All settings are optional - omit any section to use built-in defaults

# Page Layout
# Defines physical page dimensions and margins
page:
  size: letter          # Options: letter, a4, legal
  orientation: portrait # Options: portrait, landscape
  margins:
    top: 1.0           # All margins in inches
    bottom: 1.0
    left: 1.0
    right: 1.0

# Typography
# Control fonts and text sizes throughout the document
fonts:
  body: Helvetica          # Standard paragraph text
  heading: Helvetica-Bold  # All headings
  code: Courier            # Code blocks and inline code
  
  # Font sizes in points
  sizes:
    h1: 24
    h2: 18
    h3: 14
    h4: 12
    h5: 11
    h6: 10
    body: 11
    code: 9
    caption: 9

# Colors
# RGB tuples (0-255) or hex strings
colors:
  text: "#000000"         # Main body text
  headings: "#1a1a1a"     # All heading levels
  code_bg: "#f5f5f5"      # Code block background
  code_text: "#2c3e50"    # Code text color
  links: "#0066cc"        # Hyperlinks (shown as underlined text)
  table_header: "#e8e8e8" # Table header background

# Spacing
# Control whitespace between elements
spacing:
  paragraph: 12       # Points after each paragraph
  heading_before: 18  # Points before headings (creates visual breaks)
  heading_after: 6    # Points after headings
  line_height: 1.2    # Line spacing multiplier (1.0 = single, 1.5 = 1.5x, etc.)
  list_indent: 20     # Points to indent list items

# Image Settings
images:
  max_width: 6.5        # Maximum width in inches (should fit within margins)
  max_height: 9.0       # Maximum height in inches
  dpi: 150              # Resolution for rendering
  fallback_dir: null    # Optional: directory to search if image not found relative to markdown
  center_align: true    # Center images on page
  show_captions: true   # Show alt text as caption below image

# Code Block Settings
code:
  syntax_highlight: true       # Enable Pygments syntax highlighting
  theme: default               # Options: default, monokai, github, solarized
  show_line_numbers: false     # Display line numbers in code blocks
  wrap_long_lines: true        # Wrap lines that exceed page width
  background: true             # Show background color for code blocks

# Table Settings
tables:
  header_style: bold           # Style for header row: bold, normal
  grid_lines: true             # Show cell borders
  zebra_stripes: false         # Alternate row background colors
  max_col_width: 2.0           # Maximum column width in inches (prevents single column from dominating)

# Document Metadata (can be overridden by frontmatter)
metadata:
  author: null
  title: null
  subject: null
  keywords: []
```

### 3.3 Per-Document Configuration (Frontmatter)

Documents can override configuration using YAML frontmatter:

```yaml
---
title: Technical Report
author: Matthew Pausley
date: 2026-08-11

# PageForge-specific overrides
pageforge:
  fonts:
    body: Times
    heading: Times-Bold
  colors:
    headings: "#003366"
  spacing:
    paragraph: 14
---

# Document content starts here...
```

**Frontmatter merge priority:** Frontmatter > CLI config > Directory config > Home config > Defaults

---

## 4. Markdown Feature Support

### 4.1 Fully Supported Features

| Feature | Syntax | Notes |
|---------|--------|-------|
| **Headings** | `# H1` through `###### H6` | Automatic styling hierarchy |
| **Paragraphs** | Plain text separated by blank lines | Respects `spacing.paragraph` |
| **Bold** | `**text**` or `__text__` | |
| **Italic** | `*text*` or `_text_` | |
| **Strikethrough** | `~~text~~` | Requires `extra` extension |
| **Inline code** | `` `code` `` | Monospace font, subtle background |
| **Code blocks** | ` ```language ` or indented | Syntax highlighting via Pygments |
| **Unordered lists** | `- item` or `* item` | Nested lists supported |
| **Ordered lists** | `1. item` | Automatic numbering |
| **Links** | `[text](url)` | Rendered as blue underlined text with URL in parentheses |
| **Images** | `![alt](path)` | SVG, PNG, JPG supported; alt text becomes caption |
| **Blockquotes** | `> text` | Indented with left border |
| **Horizontal rules** | `---` or `***` | Thin line separator |
| **Tables** | Markdown tables | Full grid with header styling |
| **Line breaks** | Double space + newline or `<br>` | |

### 4.2 Best-Effort Features

These features are rendered but may have limitations:

| Feature | Handling | Warning Issued |
|---------|----------|----------------|
| **LaTeX math** | `$equation$` or `$$block$$` | Rendered as monospace text | Yes - "Math rendering limited" |
| **HTML tags** | `<tag>content</tag>` | Tags stripped, content rendered | Yes - "HTML stripped" |
| **Task lists** | `- [ ]` unchecked, `- [x]` checked | Rendered as regular lists with ☐/☑ symbols | No |
| **Footnotes** | `[^1]` and `[^1]: text` | Rendered at document end | No |
| **Definition lists** | Term and definition pairs | Rendered as bold term + indented definition | No |
| **Mermaid diagrams** | ` ```mermaid ` blocks | Rendered as plain text code block | Yes - "Export as SVG first" |

### 4.3 Unsupported Features

Features that cannot be rendered in static PDF:

- Interactive HTML elements (buttons, forms)
- Embedded videos
- JavaScript
- Animated GIFs (first frame rendered as static image)

All unsupported features trigger warnings during conversion with suggestions for alternatives.

---

## 5. LLM Markdown Guidance

### 5.1 Purpose

PageForge includes comprehensive documentation (`docs/llm-markdown-guide.md`) to help LLM agents generate markdown optimized for PDF conversion.

### 5.2 Guidance Document Structure

**Section 1: Quick Start for LLMs**
- Purpose statement: "When generating markdown for PageForge..."
- Best practices summary (5-7 bullet points)
- Example of well-formed document

**Section 2: Supported Markdown Reference**
- Complete syntax reference with examples
- Visual samples showing PDF output (screenshots or descriptions)
- Feature matrix (fully supported vs. best-effort vs. unsupported)

**Section 3: Image Best Practices**
- Save images alongside markdown file
- Use relative paths: `![Chart](./chart.png)` not absolute paths
- Preferred formats: SVG for diagrams, PNG for screenshots
- Recommended dimensions: 1200-1800px wide for full-width images
- Alt text becomes caption — write descriptive captions
- Example directory structure:
  ```
  reports/
    summary.md
    chart1.png
    diagram.svg
  ```

**Section 4: Code Block Recommendations**
- Specify language for syntax highlighting: ` ```python `
- Keep line length under 80 characters for readability
- Use descriptive comments
- Example rendering for common languages (Python, SQL, bash, JSON)

**Section 5: Table Guidelines**
- Keep tables to 5-6 columns maximum (readability in portrait layout)
- Use header row for column labels
- Keep cell content concise (no paragraphs in cells)
- For wide tables, suggest landscape orientation in frontmatter

**Section 6: Document Structure Templates**

**Template A: Technical Report**
```markdown
---
title: System Analysis Report
author: Claude AI
date: 2026-08-11
pageforge:
  fonts:
    body: Times
---

# Executive Summary

Brief overview...

## Background

Context and motivation...

## Analysis

### Findings

Key observations...

### Recommendations

1. First recommendation
2. Second recommendation

## Conclusion

Summary...
```

**Template B: Data Summary with Visualizations**
```markdown
---
title: Quarterly Metrics Summary
author: Analysis Bot
date: 2026-08-11
---

# Overview

This report summarizes...

## Key Metrics

![Quarterly Trends](./trends.png)

The chart above shows...

## Detailed Breakdown

| Metric | Q1 | Q2 | Q3 | Q4 |
|--------|-------|-------|-------|-------|
| Revenue | $100K | $120K | $135K | $150K |

## Analysis

...
```

**Template C: Gallery/Catalog**
```markdown
# Curve Gallery

Visual reference of all generated curves.

## Euler Spirals

### Linear Curvature

**Parameters:** `t_max = 5`

![Linear Clothoid](../output/svg/linear.svg)

The linear curvature Euler spiral...

### Quadratic Curvature

**Parameters:** `t_max = 2.5`

![Quadratic Clothoid](../output/svg/quadratic.svg)

...
```

**Section 7: Common Pitfalls**

| ❌ Avoid | ✅ Do Instead | Reason |
|----------|---------------|---------|
| `![](https://url.com/img.png)` | Save image locally and use relative path | Remote URLs not fetched |
| `<img src="..." style="...">` | Use markdown image syntax | HTML styling stripped |
| Base64-encoded images | Save as actual image file | Better performance, debuggable |
| `$$\frac{complex}{math}$$` | Simplify or export as image | Limited math rendering |
| Tables with 10+ columns | Break into multiple tables or use landscape | Readability |
| Very long code blocks (500+ lines) | Link to separate file or summarize | Page layout issues |

**Section 8: Testing Your Markdown**

```bash
# Quick test conversion
pageforge your-document.md -v

# Check for warnings
pageforge your-document.md -vv 2>&1 | grep -i warning

# Batch test
pageforge test-docs/*.md -o test-output/
```

---

## 6. Error Handling and User Experience

### 6.1 Error Categories

**1. File Errors**
- Input file not found
- Output directory not writable
- Config file malformed

**2. Content Errors**
- Invalid markdown syntax (very rare with Python-markdown)
- Corrupted images
- Unsupported image formats

**3. Configuration Errors**
- Invalid YAML syntax
- Out-of-range values (e.g., negative margins)
- Unknown configuration keys (warning, not error)

**4. Dependency Errors**
- Missing Python packages
- Incompatible package versions

### 6.2 Error Message Design Principles

- **Be specific:** "Image not found: diagram.svg" not "File error"
- **Show context:** Include file path and line number where relevant
- **Suggest solutions:** "Did you mean diagram.png?"
- **Use colors** (when terminal supports): Red for errors, yellow for warnings
- **Exit cleanly:** Always provide appropriate exit code

### 6.3 Warning System

Warnings don't stop conversion but inform user of limitations:

```
[WARNING] Math equation rendering is limited (line 42)
  Found: $\frac{x^2}{y}$
  Rendered as: monospace text
  Tip: For complex math, consider rendering equation as SVG image

[WARNING] HTML tag stripped (line 67)
  Found: <div style="color: red">
  Rendered: content only, styling ignored
```

**Warning verbosity levels:**
- Default: Show count of warnings, suppress details
- `-v`: Show all warnings with context
- `-vv`: Show warnings + debug info (image paths resolved, style applied, etc.)
- `--quiet`: Suppress warnings entirely

### 6.4 Progress Feedback

For batch processing, show progress:

```
Converting markdown files...
  ✓ report1.md → report1.pdf (2.3s)
  ✓ report2.md → report2.pdf (1.8s)
  ⚠ report3.md → report3.pdf (3.1s) - 2 warnings
  ✗ report4.md - Failed: missing image chart.png

Summary: 3 succeeded, 1 failed, 2 warnings
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

**Parser Module:**
- Markdown parsing correctness
- Frontmatter extraction
- Image reference detection
- Warning generation for unsupported features

**Image Resolver:**
- Path resolution logic (relative, fallback)
- SVG loading and conversion
- Raster image loading with size constraints
- User prompt simulation

**Configuration:**
- Config loading from multiple sources
- Config merging (defaults + user)
- Validation of config values
- Schema compliance

**Generator:**
- Individual element rendering (headings, paragraphs, lists, etc.)
- Style application
- Page layout calculations

### 7.2 Integration Tests

**End-to-End Conversions:**
- Convert sample documents and verify PDF structure
- Test with various markdown features (tables, code, images)
- Test with different configurations
- Test batch processing

**Fixtures:**
```
tests/fixtures/
  basic-document.md
  with-images.md
  complex-tables.md
  code-samples.md
  math-heavy.md (test warnings)
  frontmatter-override.md
  images/
    test-diagram.svg
    test-chart.png
```

**Assertions:**
- PDF generated successfully (file exists, not empty)
- PDF is valid (can be opened by readers)
- Expected number of pages
- Warning count matches expected
- Specific elements present (verify text content in PDF)

### 7.3 Visual Regression Testing

For major releases, generate PDFs from fixed markdown fixtures and manually review:
- Typography consistency
- Image scaling and positioning
- Code block formatting
- Table rendering
- Page breaks in sensible locations

Store reference PDFs in `tests/visual-references/` for comparison.

### 7.4 Test Coverage Goals

- Unit test coverage: >85%
- Integration test coverage: All major features
- Error path coverage: All error types and warnings

---

## 8. Implementation Phases

### Phase 1: Foundation (MVP)
**Goal:** Basic markdown → PDF conversion with default styling

**Deliverables:**
- CLI entry point with basic commands
- Markdown parser (headings, paragraphs, lists, bold/italic)
- PDF generator with simple styling
- Default configuration
- Basic image support (PNG/JPG, relative paths only)
- Unit tests for core functionality

**Success Criteria:**
- Convert simple markdown document to readable PDF
- `pageforge document.md` works end-to-end

### Phase 2: Enhanced Markdown Support
**Goal:** Handle complex markdown features

**Deliverables:**
- Code blocks with syntax highlighting (Pygments)
- Tables rendering
- Blockquotes and horizontal rules
- SVG image support (svglib)
- Inline formatting (strikethrough, inline code)
- Warning system for unsupported features

**Success Criteria:**
- Convert complex markdown documents with all common features
- Appropriate warnings for edge cases

### Phase 3: Configuration System
**Goal:** User customization and styling control

**Deliverables:**
- YAML configuration loading and merging
- Frontmatter support for per-document config
- `--init-config` command to generate template
- `--show-config` command
- Extensive inline documentation in config file
- Configuration validation

**Success Criteria:**
- Users can customize fonts, colors, spacing via config file
- Frontmatter overrides work correctly
- Config errors provide helpful messages

### Phase 4: Image Handling & UX Polish
**Goal:** Robust image resolution and user experience

**Deliverables:**
- Image path resolution (relative + fallback directory)
- Interactive prompts for missing images
- `--no-prompt` flag for non-interactive use
- Batch processing (`pageforge *.md`)
- Verbose/quiet output modes
- Progress feedback for batch conversions
- Comprehensive error messages

**Success Criteria:**
- Missing images handled gracefully with user prompts
- Batch processing works smoothly
- Error messages are helpful and actionable

### Phase 5: Documentation & LLM Guidance
**Goal:** Comprehensive documentation for users and LLMs

**Deliverables:**
- User guide (installation, basic usage, examples)
- Configuration reference
- LLM markdown guidance document
- Example markdown documents and templates
- README with quick start

**Success Criteria:**
- First-time user can install and convert a document in <5 minutes
- LLM can generate PageForge-optimized markdown from guidance doc
- All configuration options documented

### Phase 6: Testing & Packaging
**Goal:** Robust, distributable package

**Deliverables:**
- Comprehensive test suite (unit + integration)
- Test fixtures covering all features
- CI/CD setup (GitHub Actions)
- PyPI packaging (`pip install pageforge`)
- Installation instructions for Windows

**Success Criteria:**
- >85% test coverage
- All tests passing on Windows
- Package installable via pip
- CLI available after install (`pageforge --help`)

---

## 9. Future Enhancements (Post-V1)

### LaTeX Output
- Add `pageforge document.md --format latex` option
- Generate `.tex` file instead of PDF
- Allows advanced users to customize further in LaTeX editors

### Advanced Features
- Table of contents generation (`--toc` flag)
- Multi-column layouts (for newsletters/academic papers)
- Custom headers/footers with page numbers
- Watermarks
- PDF bookmarks from headings

### Math Rendering
- Integrate `matplotlib` or `sympy` to render LaTeX equations as images
- Embed rendered equations in PDF

### Template System
- Pre-built templates (report, memo, academic paper)
- `pageforge document.md --template academic`
- User-defined templates via config

### Watch Mode
- `pageforge document.md --watch`
- Auto-regenerate PDF when markdown changes
- Useful during document authoring

### Performance Optimization
- Parallel processing for batch conversions
- Caching of parsed markdown and processed images
- Incremental updates for large documents

---

## 10. Dependencies and Installation

### 10.1 Python Version

**Minimum:** Python 3.10  
**Tested:** Python 3.10, 3.11, 3.12, 3.13

### 10.2 Required Dependencies

```toml
# pyproject.toml dependencies
[project]
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
```

### 10.3 Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
```

### 10.4 Installation Methods

**From PyPI (post-release):**
```bash
pip install pageforge
```

**From source:**
```bash
git clone https://github.com/medmond78/PageForge.git
cd PageForge
pip install -e .
```

**For development:**
```bash
pip install -e ".[dev]"
```

---

## 11. Success Metrics

### 11.1 Technical Metrics

- **Conversion success rate:** >95% for well-formed markdown
- **Performance:** <5 seconds for typical document (10 pages, 5 images)
- **Test coverage:** >85%
- **Dependency count:** <10 direct dependencies

### 11.2 User Experience Metrics

- **Time to first PDF:** <5 minutes from installation
- **Configuration discoverability:** Users find `--init-config` within first use
- **Error resolution:** Clear next steps in >90% of error messages

### 11.3 LLM Integration Metrics

- **Claude Code compatibility:** All CLI commands work via Bash tool
- **LLM guidance effectiveness:** LLMs generate compatible markdown >95% of time after reading guide

---

## 12. Open Questions and Decisions

### ✅ Resolved

1. **Q:** Use Pandoc or pure Python?  
   **A:** Pure Python (ReportLab) to avoid external dependencies and IT headaches

2. **Q:** Configuration format?  
   **A:** YAML with extensive inline docs and sensible defaults

3. **Q:** How to handle missing images?  
   **A:** Interactive prompts in normal mode, fail with error in `--no-prompt` mode

4. **Q:** CLI framework?  
   **A:** Click (more features than argparse, well-documented)

### ⏳ Future Decisions

1. **Q:** Should we support custom ReportLab styles directly (for advanced users)?  
   **A:** Defer to post-V1; YAML config should handle 95% of use cases

2. **Q:** How to handle very large documents (100+ pages)?  
   **A:** Test performance in Phase 6, optimize if needed (streaming, chunking)

3. **Q:** Should we embed fonts for non-standard typefaces?  
   **A:** V1 uses ReportLab built-in fonts; custom font embedding in future release

---

## 13. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| ReportLab limitations for complex tables | Medium | Medium | Test early; fall back to simpler table rendering if needed |
| SVG compatibility issues (svglib) | Medium | Low | Document SVG limitations; provide test suite of SVGs |
| Windows-specific path issues | High | Medium | Extensive Windows testing; use pathlib consistently |
| Performance with large images | Low | Low | Image scaling/compression before PDF embedding |
| Configuration complexity overwhelming users | Medium | Low | Extensive documentation; defaults handle 80% of cases |
| LLM-generated markdown edge cases | Medium | Medium | Comprehensive guidance doc; iterate based on real usage |

---

## Appendices

### Appendix A: ReportLab Primer

ReportLab is a mature Python library for PDF generation. Key concepts:

- **Canvas:** Low-level API for drawing shapes, text, images
- **Platypus:** High-level framework for flowing content (what we'll use)
- **Flowables:** Content elements (Paragraph, Image, Table, Spacer, etc.)
- **Styles:** ParagraphStyle and TableStyle objects define formatting
- **DocTemplate:** Page layout manager (handles margins, page breaks)

**Why Platypus for PageForge:**
- Automatically handles page breaks
- Manages vertical spacing
- Supports complex layouts without manual coordinate calculations
- Perfect for document-style content (vs. forms or certificates)

### Appendix B: Example CLI Session

```bash
# First time setup
$ pip install pageforge
$ pageforge --init-config
Created: pageforge.yaml

# Basic conversion
$ pageforge report.md
Converting: report.md
  ✓ Parsed markdown (34 elements)
  ✓ Resolved 3 images
  ✓ Generated PDF (5 pages)
Created: report.pdf

# With missing image
$ pageforge analysis.md
Converting: analysis.md
  ✓ Parsed markdown (28 elements)
  
Warning: Image not found: missing-chart.png
  Referenced in: analysis.md line 67

Search locations checked:
  1. C:\Users\matthew\Documents\analysis\missing-chart.png

Enter image path (or 'skip' to omit, 'abort' to cancel): C:\Users\matthew\Desktop\chart.png
  ✓ Resolved 4 images
  ✓ Generated PDF (4 pages)
Created: analysis.pdf

# Batch conversion
$ pageforge reports/*.md -o output/
Converting 5 files...
  ✓ summary.md → output/summary.pdf (2.1s)
  ✓ details.md → output/details.pdf (3.4s)
  ✓ appendix.md → output/appendix.pdf (1.8s)
  ⚠ draft.md → output/draft.pdf (2.6s) - 3 warnings
  ✓ notes.md → output/notes.pdf (1.2s)

Summary: 5 succeeded, 0 failed, 3 warnings
Total time: 11.1s

# View warnings
$ pageforge draft.md -v
Converting: draft.md
  ✓ Parsed markdown (42 elements)
  
[WARNING] Math equation rendering is limited (line 23)
  Found: $$\int_0^1 f(x)dx$$
  Rendered as: monospace text
  Tip: For complex math, consider rendering as SVG
  
[WARNING] HTML tag stripped (line 45)
  Found: <span style="color: red">Important</span>
  Rendered: Important (styling ignored)
  
[WARNING] Unsupported diagram type (line 78)
  Found: mermaid code block
  Rendered as: plain text code block
  Tip: Export mermaid diagram as SVG, embed as image
  
  ✓ Resolved 2 images
  ✓ Generated PDF (6 pages)
Created: draft.pdf (3 warnings)
```

### Appendix C: Sample Output Structure

When converting `report.md` in `C:\Users\matthew\Documents\`:

**Default output (same directory):**
```
C:\Users\matthew\Documents\
  report.md
  report.pdf          <- created here
  chart.png
  diagram.svg
```

**Explicit output file:**
```bash
$ pageforge report.md -o final-report.pdf

C:\Users\matthew\Documents\
  report.md
  final-report.pdf    <- created here
  chart.png
```

**Output directory:**
```bash
$ pageforge report.md -o C:\Output\

C:\Output\
  report.pdf          <- created here
```

**Batch with output directory:**
```bash
$ pageforge *.md -o output/

output/
  report1.pdf
  report2.pdf
  analysis.pdf
```

---

## Why This Design

**1. Pure Python Approach**  
Avoids Node/npm (user's stated constraint), external binaries (Pandoc), and system libraries (WeasyPrint). Everything installs cleanly via pip on IT-managed machines.

**2. Configuration via YAML**  
More readable than JSON, supports comments for inline documentation. Familiar to developers and LLMs. Merging strategy (defaults → home → project → CLI → frontmatter) provides flexibility without complexity.

**3. Interactive Image Resolution**  
Gracefully handles the common case of LLM-generated markdown referencing images that may be in different directories. User can fix paths interactively rather than failing conversion.

**4. LLM Guidance Document**  
Treating LLMs as first-class users ensures generated markdown works well with PageForge. Reduces friction when using Claude Code to generate reports automatically.

**5. Phased Implementation**  
MVP first (basic conversion), then enhancements. Ensures early delivery of working tool, with iterative improvements based on real usage.

**6. Comprehensive Documentation**  
Casual users need clear examples and defaults that "just work". Advanced users need full configuration reference. Both needs met through layered documentation approach.

---

**Why ReportLab over alternatives:**

| Tool | Pros | Cons | Decision |
|------|------|------|----------|
| **ReportLab** | Pure Python, pip-installable, no external deps, full control | More dev work for complex features | ✅ **Selected** |
| **Pandoc** | Excellent markdown support, LaTeX quality | Requires binary + LaTeX, subprocess complexity | ❌ External dependency issues |
| **WeasyPrint** | Great HTML/CSS rendering | Requires Cairo/Pango on Windows (difficult install) | ❌ System library headaches |
| **pdfkit** | Simple HTML → PDF | Requires wkhtmltopdf binary | ❌ External binary |
| **FPDF** | Lightweight | Limited features, less mature than ReportLab | ❌ Less capable |

**How to apply:**  
This design balances user needs (IT constraints, ease of use) with technical requirements (extensibility, maintainability). Implementation should follow the phased approach, delivering a working MVP before adding complexity.

---

**End of Design Specification**
