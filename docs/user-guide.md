# PageForge User Guide

Complete guide to converting Markdown documents to PDF with PageForge.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [CLI Reference](#cli-reference)
4. [Configuration](#configuration)
5. [Markdown Support](#markdown-support)
6. [Image Handling](#image-handling)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)
9. [Tips for LLM-Generated Markdown](#tips-for-llm-generated-markdown)

---

## Installation

### Prerequisites

PageForge requires Python 3.10 or higher. Check your Python version:

```bash
python --version
```

### Install from Source

Clone the repository and install:

```bash
git clone https://github.com/medmond78/PageForge.git
cd PageForge
pip install -e .
```

### Verify Installation

After installation, the `pageforge` command should be available:

```bash
pageforge --help
```

You should see the help message with available options.

---

## Quick Start

### Basic Conversion

Convert a markdown file to PDF with default settings:

```bash
pageforge document.md
```

This creates `document.pdf` in the same directory as `document.md`.

### Specify Output Location

Provide an output path:

```bash
# Specific output file
pageforge document.md -o report.pdf

# Output to a directory
pageforge document.md -o ./output/

# Absolute path
pageforge document.md -o C:\Reports\final.pdf
```

### Example Workflow

1. Create a markdown file `report.md`:

```markdown
# My Report

This is a test document with **bold** and *italic* text.

## Section 1

Here's some content with a list:

- Item 1
- Item 2
- Item 3
```

2. Convert to PDF:

```bash
pageforge report.md
```

3. Open `report.pdf` to view the result.

---

## CLI Reference

### Command Syntax

```bash
pageforge INPUT_FILE [OUTPUT_FILE] [OPTIONS]
```

### Arguments

#### `INPUT_FILE` (required)

Path to the markdown file to convert.

```bash
pageforge document.md
```

#### `OUTPUT_FILE` (optional)

Path to the output PDF file. If omitted, uses the input filename with `.pdf` extension.

```bash
# Creates document.pdf
pageforge document.md

# Creates custom-name.pdf
pageforge document.md custom-name.pdf

# Creates report.pdf
pageforge document.md -o report.pdf
```

### Options

#### `--config CONFIG_FILE`

Use a custom YAML configuration file instead of the default.

```bash
pageforge document.md --config custom-config.yaml
```

Configuration files define fonts, colors, spacing, and layout. See [Configuration](#configuration) for details.

#### `--no-prompt` / `-n`

Disable interactive prompts for missing images. If any images are missing, the conversion will fail with exit code 2.

```bash
pageforge document.md --no-prompt
pageforge document.md -n
```

This is useful for:
- Automated workflows
- CI/CD pipelines
- Batch processing scripts

Without this flag, PageForge will prompt you to provide paths for missing images interactively.

#### `--help`

Display help message with all available options.

```bash
pageforge --help
```

### Exit Codes

PageForge uses standard exit codes:

- `0` - Success
- `1` - Conversion failed (invalid markdown, file errors, configuration errors)
- `2` - Missing images in non-interactive mode (`--no-prompt`)

---

## Configuration

PageForge uses YAML configuration files to customize PDF output. Configuration is entirely optional - the tool works with sensible defaults.

### Configuration Discovery

PageForge looks for configuration in this order:

1. `--config` command-line argument
2. `pageforge.yaml` in the current directory
3. `.pageforge.yaml` in your home directory
4. Built-in defaults

Each level overrides the previous, so you can have project-specific settings that override global defaults.

### Configuration File Format

Create a `pageforge.yaml` file with any or all of these sections:

```yaml
# Page Layout
page:
  size: letter          # Options: letter, a4, legal
  orientation: portrait # Options: portrait, landscape
  margins:
    top: 1.0           # All margins in inches
    bottom: 1.0
    left: 1.0
    right: 1.0

# Typography
fonts:
  body: Helvetica          # Font for body text
  heading: Helvetica-Bold  # Font for all headings
  code: Courier            # Font for code blocks
  
  sizes:                   # All sizes in points
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
colors:
  text: "#000000"         # Main body text (hex format)
  headings: "#1a1a1a"     # All heading levels
  code_bg: "#f5f5f5"      # Code block background
  code_text: "#2c3e50"    # Code text color
  links: "#0066cc"        # Hyperlinks
  table_header: "#e8e8e8" # Table header background

# Spacing
spacing:
  paragraph: 12       # Points after each paragraph
  heading_before: 18  # Points before headings
  heading_after: 6    # Points after headings
  line_height: 1.2    # Line spacing multiplier
  list_indent: 20     # Points to indent list items

# Image Settings
images:
  max_width: 6.5        # Maximum width in inches
  max_height: 9.0       # Maximum height in inches
  dpi: 150              # Resolution for rendering
  fallback_dir: null    # Optional: directory for image search
  center_align: true    # Center images on page
  show_captions: true   # Show alt text as caption

# Code Block Settings
code:
  syntax_highlight: true       # Enable Pygments syntax highlighting
  theme: default               # Syntax theme (default, monokai, etc.)
  show_line_numbers: false     # Display line numbers
  wrap_long_lines: true        # Wrap lines that exceed page width
  background: true             # Show background color
```

### Configuration Options Reference

#### Page Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `page.size` | string | `letter` | Paper size: `letter`, `a4`, or `legal` |
| `page.orientation` | string | `portrait` | Page orientation: `portrait` or `landscape` |
| `page.margins.top` | float | `1.0` | Top margin in inches |
| `page.margins.bottom` | float | `1.0` | Bottom margin in inches |
| `page.margins.left` | float | `1.0` | Left margin in inches |
| `page.margins.right` | float | `1.0` | Right margin in inches |

#### Font Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `fonts.body` | string | `Helvetica` | Font for body text |
| `fonts.heading` | string | `Helvetica-Bold` | Font for headings |
| `fonts.code` | string | `Courier` | Font for code blocks |
| `fonts.sizes.h1` | int | `24` | H1 heading size in points |
| `fonts.sizes.h2` | int | `18` | H2 heading size in points |
| `fonts.sizes.h3` | int | `14` | H3 heading size in points |
| `fonts.sizes.h4` | int | `12` | H4 heading size in points |
| `fonts.sizes.h5` | int | `11` | H5 heading size in points |
| `fonts.sizes.h6` | int | `10` | H6 heading size in points |
| `fonts.sizes.body` | int | `11` | Body text size in points |
| `fonts.sizes.code` | int | `9` | Code block text size in points |
| `fonts.sizes.caption` | int | `9` | Image caption size in points |

Available fonts (ReportLab built-in):
- `Helvetica`, `Helvetica-Bold`, `Helvetica-Oblique`, `Helvetica-BoldOblique`
- `Times-Roman`, `Times-Bold`, `Times-Italic`, `Times-BoldItalic`
- `Courier`, `Courier-Bold`, `Courier-Oblique`, `Courier-BoldOblique`

#### Color Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `colors.text` | string | `#000000` | Body text color (hex) |
| `colors.headings` | string | `#1a1a1a` | Heading text color (hex) |
| `colors.code_bg` | string | `#f5f5f5` | Code block background (hex) |
| `colors.code_text` | string | `#2c3e50` | Code text color (hex) |
| `colors.links` | string | `#0066cc` | Link color (hex) |
| `colors.table_header` | string | `#e8e8e8` | Table header background (hex) |

Colors should be in hex format: `#RRGGBB`

#### Spacing Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `spacing.paragraph` | int | `12` | Space after paragraphs (points) |
| `spacing.heading_before` | int | `18` | Space before headings (points) |
| `spacing.heading_after` | int | `6` | Space after headings (points) |
| `spacing.line_height` | float | `1.2` | Line height multiplier |
| `spacing.list_indent` | int | `20` | List item indentation (points) |

#### Image Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `images.max_width` | float | `6.5` | Maximum image width (inches) |
| `images.max_height` | float | `9.0` | Maximum image height (inches) |
| `images.dpi` | int | `150` | Image resolution |
| `images.fallback_dir` | string | `null` | Fallback directory for images |
| `images.center_align` | bool | `true` | Center images on page |
| `images.show_captions` | bool | `true` | Show alt text as caption |

#### Code Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `code.syntax_highlight` | bool | `true` | Enable syntax highlighting |
| `code.theme` | string | `default` | Pygments theme name |
| `code.show_line_numbers` | bool | `false` | Show line numbers |
| `code.wrap_long_lines` | bool | `true` | Wrap long code lines |
| `code.background` | bool | `true` | Show background color |

### Per-Document Configuration

You can override configuration for individual documents using YAML frontmatter:

```yaml
---
title: Technical Report
author: Your Name
date: 2026-08-12

# PageForge-specific overrides
pageforge:
  fonts:
    body: Times-Roman
    heading: Times-Bold
  colors:
    headings: "#003366"
  spacing:
    paragraph: 14
---

# Document content starts here
```

Frontmatter settings override all other configuration sources.

---

## Markdown Support

PageForge supports standard Markdown with extensions via the Python `markdown` library.

### Fully Supported Features

#### Headings

Six levels of headings using `#` syntax:

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

#### Text Formatting

```markdown
**Bold text** or __bold text__
*Italic text* or _italic text_
***Bold and italic*** or ___bold and italic___
`Inline code`
```

#### Paragraphs

Separate paragraphs with blank lines:

```markdown
This is paragraph one.

This is paragraph two.
```

#### Lists

Unordered lists using `-`, `*`, or `+`:

```markdown
- Item 1
- Item 2
  - Nested item 2.1
  - Nested item 2.2
- Item 3
```

Ordered lists using numbers:

```markdown
1. First item
2. Second item
   1. Nested item 2.1
   2. Nested item 2.2
3. Third item
```

#### Code Blocks

Fenced code blocks with optional language:

````markdown
```python
def hello():
    print("Hello, world!")
```
````

Supported languages include Python, JavaScript, Java, C, C++, Go, Rust, SQL, Bash, JSON, YAML, HTML, CSS, and many more via Pygments.

#### Tables

Markdown tables with optional alignment:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

| Left | Center | Right |
|:-----|:------:|------:|
| L1   | C1     | R1    |
| L2   | C2     | R2    |
```

#### Images

Images using standard markdown syntax:

```markdown
![Alt text description](path/to/image.png)
![Diagram](./diagram.svg)
```

Supported formats: PNG, JPG, JPEG, SVG

#### Blockquotes

Use `>` for blockquotes:

```markdown
> This is a blockquote.
> It can span multiple lines.

> > Nested blockquotes are also supported.
```

#### Horizontal Rules

Create horizontal rules with three or more `-`, `*`, or `_`:

```markdown
---
***
___
```

#### Links

Standard markdown links:

```markdown
[Link text](https://example.com)
```

Links are rendered as blue underlined text with the URL in parentheses (since PDFs are static).

### Limitations

PageForge has some limitations compared to full HTML rendering:

#### Not Supported

- Interactive HTML elements (buttons, forms)
- Embedded videos
- JavaScript
- Animated GIFs (only first frame rendered)
- LaTeX math (rendered as plain text)
- Mermaid diagrams (rendered as plain code block)

#### Workarounds

For unsupported features:

- **Math equations**: Render as images (PNG/SVG) and embed
- **Diagrams (Mermaid/PlantUML)**: Export as SVG and embed
- **Interactive content**: Not applicable to static PDF

---

## Image Handling

PageForge provides flexible image resolution with interactive prompts.

### Image Paths

Use relative paths in your markdown:

```markdown
![Chart](./chart.png)
![Diagram](../images/diagram.svg)
```

### Resolution Strategy

When PageForge encounters an image reference, it searches in this order:

1. Path relative to the markdown file directory
2. Fallback directory (if configured via `images.fallback_dir`)
3. Interactive prompt (if enabled)

### Interactive Mode

By default, PageForge prompts for missing images:

```
Warning: Image not found: diagram.svg
  Referenced in: document.md

Search locations checked:
  1. C:\Documents\diagram.svg (relative to markdown)
  2. C:\Images\diagram.svg (from fallback_dir)

Enter image path (or 'skip' to omit, 'abort' to cancel): _
```

You can:
- Enter a full path to the image
- Type `skip` to omit the image and continue
- Type `abort` to cancel the conversion

### Non-Interactive Mode

For automated workflows, use `--no-prompt`:

```bash
pageforge document.md --no-prompt
```

If images are missing, the conversion fails with exit code 2.

### Fallback Directory

Configure a fallback directory for images:

```yaml
images:
  fallback_dir: C:\Images\
```

PageForge will search this directory if images aren't found relative to the markdown file.

### Image Formats

| Format | Support | Notes |
|--------|---------|-------|
| PNG | Full | Recommended for screenshots |
| JPG/JPEG | Full | Recommended for photos |
| SVG | Full | Recommended for diagrams, charts |
| GIF | Partial | Only first frame rendered |
| BMP | Not supported | Convert to PNG first |

### Image Best Practices

1. **Use relative paths**: `./image.png` not `C:\Full\Path\image.png`
2. **Keep images near markdown**: Store in same directory or subdirectory
3. **Use appropriate formats**:
   - SVG for diagrams, charts, logos
   - PNG for screenshots, graphics with transparency
   - JPG for photos
4. **Optimize image sizes**: Large images (>2MB) may slow conversion
5. **Use descriptive alt text**: It becomes the caption

Example directory structure:

```
project/
  report.md
  chart.png
  diagram.svg
  images/
    screenshot1.png
    screenshot2.png
```

In `report.md`:

```markdown
![Monthly Revenue Chart](./chart.png)
![System Architecture](./diagram.svg)
![Login Screen](./images/screenshot1.png)
```

---

## Examples

### Example 1: Simple Report

`report.md`:

```markdown
# Monthly Sales Report

## Executive Summary

This report summarizes sales performance for August 2026.

**Key findings:**

- Total revenue: $150,000
- Growth: 12% over July
- Top product: Widget Pro

## Detailed Analysis

### Revenue Breakdown

| Product | Units Sold | Revenue |
|---------|------------|---------|
| Widget Pro | 1,200 | $60,000 |
| Widget Plus | 800 | $40,000 |
| Widget Basic | 1,000 | $50,000 |

### Trends

Revenue has shown consistent growth over the past three months:

1. June: $120,000
2. July: $134,000
3. August: $150,000

## Conclusion

Strong performance across all product lines. Continue current strategy.
```

Convert:

```bash
pageforge report.md
```

### Example 2: Technical Documentation

`api-guide.md`:

```markdown
# API Documentation

## Authentication

All API requests require authentication via API key:

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}

response = requests.get(
    "https://api.example.com/data",
    headers=headers
)
```

## Endpoints

### GET /users

Retrieve user list.

**Parameters:**

- `limit` (int): Maximum number of results
- `offset` (int): Pagination offset

**Response:**

```json
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "total": 42
}
```

### POST /users

Create a new user.

**Request Body:**

```json
{
  "name": "Charlie",
  "email": "charlie@example.com"
}
```
```

Convert with custom config:

`pageforge.yaml`:

```yaml
fonts:
  body: Courier
  sizes:
    body: 10
    code: 8

colors:
  headings: "#003366"
  code_bg: "#f0f0f0"
```

```bash
pageforge api-guide.md --config pageforge.yaml
```

### Example 3: Document with Images

`analysis.md`:

```markdown
# Data Analysis Results

## Overview

This analysis covers customer behavior patterns.

## Key Visualizations

### Traffic Over Time

![Traffic Chart](./charts/traffic.png)

The chart above shows steady growth in daily active users.

### User Demographics

![Demographics](./charts/demographics.svg)

Most users are in the 25-34 age range.

## Recommendations

Based on the data:

1. Focus marketing on 25-34 demographic
2. Optimize for mobile (60% of traffic)
3. Expand content in popular categories
```

Directory structure:

```
project/
  analysis.md
  charts/
    traffic.png
    demographics.svg
```

Convert:

```bash
pageforge analysis.md
```

### Example 4: Custom Styling with Frontmatter

`styled-report.md`:

```yaml
---
title: Quarterly Review
author: Jane Doe
date: 2026-08-12

pageforge:
  page:
    orientation: landscape
  fonts:
    body: Times-Roman
    heading: Times-Bold
    sizes:
      h1: 28
      body: 12
  colors:
    headings: "#800000"
    text: "#333333"
  spacing:
    paragraph: 14
---

# Quarterly Review

Content here...
```

The frontmatter settings override the default configuration for this document only.

---

## Troubleshooting

### Common Issues

#### "Command not found: pageforge"

**Problem:** The CLI is not in your PATH.

**Solution:** Reinstall with pip and verify:

```bash
pip install -e .
pageforge --help
```

#### "Image not found" Errors

**Problem:** Images referenced in markdown cannot be located.

**Solutions:**

1. Use relative paths: `![Image](./image.png)` not absolute paths
2. Verify image files exist in the expected location
3. Configure a fallback directory:

```yaml
images:
  fallback_dir: C:\Images\
```

4. Use interactive mode (default) to provide paths manually

#### "Invalid YAML in config file"

**Problem:** Configuration file has syntax errors.

**Solutions:**

1. Check YAML syntax (indentation, colons, quotes)
2. Validate with a YAML linter
3. Start with a minimal config and add sections incrementally

Example minimal config:

```yaml
fonts:
  body: Helvetica
  
colors:
  headings: "#003366"
```

#### "Failed to generate PDF"

**Problem:** Error during PDF generation.

**Possible causes:**

1. **Corrupted images**: Verify image files open correctly
2. **Invalid configuration values**: Check numeric values are in valid ranges
3. **Very large documents**: Try splitting into multiple files
4. **Memory issues**: Close other applications and try again

#### Code Blocks Not Highlighted

**Problem:** Code blocks appear as plain text without syntax highlighting.

**Solutions:**

1. Specify language in code fence:

````markdown
```python
code here
```
````

2. Verify `code.syntax_highlight` is `true` in config:

```yaml
code:
  syntax_highlight: true
```

3. Check that Pygments supports the language (most common languages are supported)

#### Tables Look Misaligned

**Problem:** Table columns are uneven or overflow page.

**Solutions:**

1. Keep tables to 5-6 columns maximum
2. Use shorter cell content
3. Consider landscape orientation for wide tables:

```yaml
page:
  orientation: landscape
```

4. Split wide tables into multiple smaller tables

### Getting Help

If you encounter issues not covered here:

1. Check the [design specification](docs/superpowers/specs/2026-08-11-pageforge-design.md) for technical details
2. Verify all dependencies are installed: `pip install -e .`
3. Try with a minimal markdown file to isolate the issue
4. Open an issue on GitHub with:
   - Your markdown file (or minimal example)
   - Configuration file (if using custom config)
   - Full error message
   - Python version and OS

---

## Tips for LLM-Generated Markdown

PageForge is optimized for LLM-generated content. Follow these guidelines when generating markdown programmatically.

### Directory Structure

Organize files with images in predictable locations:

```
project/
  report.md
  image1.png
  image2.svg
```

Or use a subdirectory:

```
project/
  report.md
  images/
    chart1.png
    diagram.svg
```

### Image References

Always use relative paths:

```markdown
![Chart](./chart.png)
![Diagram](./images/diagram.svg)
```

Never use absolute paths or remote URLs:

```markdown
![Bad](C:\Full\Path\image.png)
![Bad](https://example.com/image.png)
```

### Code Blocks

Specify language for syntax highlighting:

````markdown
```python
def process_data(data):
    return [x * 2 for x in data]
```
````

Keep lines under 80 characters for readability.

### Tables

Keep tables concise for portrait layout:

```markdown
| Metric | Value | Change |
|--------|-------|--------|
| Revenue | $150K | +12% |
| Users | 1,200 | +8% |
```

For wider tables, use frontmatter to set landscape:

```yaml
---
pageforge:
  page:
    orientation: landscape
---
```

### Alt Text

Provide descriptive alt text for images (becomes caption):

```markdown
![Monthly revenue trends showing 12% growth from July to August](./revenue-chart.png)
```

Not:

```markdown
![image](./revenue-chart.png)
```

### Document Structure

Use consistent heading hierarchy:

```markdown
# Main Title (H1)

## Section (H2)

### Subsection (H3)

Content...

## Next Section (H2)
```

Don't skip levels (e.g., H1 directly to H3).

### Line Length

Keep paragraph line length reasonable (no single-line paragraphs with 500 characters). Use natural line breaks:

```markdown
This is a paragraph with reasonable line length.
It's easier to read and edit.

This is another paragraph.
```

### Special Characters

Most special characters work fine. For characters that might conflict with markdown syntax, use HTML entities if needed:

- `&lt;` for <
- `&gt;` for >
- `&amp;` for &

### Testing

After generating markdown:

1. Convert with PageForge
2. Open PDF and verify formatting
3. Check that images are embedded correctly
4. Verify code blocks have proper syntax highlighting

### Example Template

Here's a complete template for LLM-generated reports:

```markdown
---
title: Report Title
author: Generated by Claude
date: 2026-08-12
---

# Report Title

## Executive Summary

Brief overview of key findings.

## Detailed Analysis

### Section 1

Content with **bold** and *italic* formatting.

![Relevant Chart](./chart.png)

The chart above shows...

### Section 2

More analysis with a table:

| Metric | Q1 | Q2 | Q3 |
|--------|-----|-----|-----|
| Revenue | $100K | $120K | $150K |

And a code example:

```python
def analyze_data(data):
    """Process and analyze data."""
    results = process(data)
    return results
```

## Conclusion

Summary of findings and recommendations:

1. First recommendation
2. Second recommendation
3. Third recommendation

---

**Report generated:** 2026-08-12
```

### Validation

Before converting, verify:

- All image paths are relative and files exist
- Code blocks specify language
- Tables fit in portrait orientation (or set landscape)
- No unsupported features (embedded video, JavaScript)
- Frontmatter YAML is valid
- Alt text is descriptive

Following these guidelines ensures smooth conversion from markdown to PDF.

---

## Advanced Usage

### Batch Processing

While PageForge doesn't have built-in batch processing, you can process multiple files with a shell script:

**Bash:**

```bash
for file in *.md; do
    pageforge "$file" -o "output/${file%.md}.pdf"
done
```

**PowerShell:**

```powershell
Get-ChildItem -Filter *.md | ForEach-Object {
    pageforge $_.FullName -o "output\$($_.BaseName).pdf"
}
```

### Custom Configuration per Project

Create a `pageforge.yaml` in each project directory for consistent styling:

```
project-a/
  pageforge.yaml  # Corporate style
  document.md

project-b/
  pageforge.yaml  # Technical style
  api-docs.md
```

### Integration with Claude Code

PageForge integrates seamlessly with Claude Code workflows:

```bash
# Generate markdown with Claude Code
claude "Create a summary report of recent changes"

# Convert to PDF
pageforge summary.md
```

For automated workflows, use `--no-prompt`:

```bash
pageforge report.md -n || echo "Conversion failed - check images"
```

---

**End of User Guide**

For technical details, see the [Design Specification](superpowers/specs/2026-08-11-pageforge-design.md).
