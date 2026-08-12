# PageForge Style Gallery

Alternative style configurations for different document types.

## Available Styles

### LaTeX Article Style (`latex-style.yaml`)

Mimics the classic LaTeX article document class appearance.

**Characteristics:**
- Serif font (Times-Roman) for body text
- Pure black text and headings (traditional LaTeX)
- Generous side margins (1.25 inches)
- Tighter line spacing (1.2)
- Minimalist aesthetic

**Best for:**
- Academic papers
- Research reports
- Technical documentation requiring traditional look
- Documents destined for print

**Usage:**
```bash
pageforge document.md output.pdf --config examples/styles/latex-style.yaml
```

### Modern Minimal Style (`modern-minimal.yaml`)

Clean, contemporary look with generous whitespace.

**Characteristics:**
- Sans-serif fonts (Helvetica)
- Dark blue-gray text (#2c3e50) - easier on eyes
- Large headings (up to 24pt)
- Generous line spacing (1.6) and paragraph spacing
- Lots of whitespace

**Best for:**
- Executive summaries
- Presentations-turned-documents
- Marketing materials
- Documents emphasizing readability over density

**Usage:**
```bash
pageforge document.md output.pdf --config examples/styles/modern-minimal.yaml
```

### Technical Report Style (`technical-report.yaml`)

Professional style for engineering and scientific documents.

**Characteristics:**
- Serif body text (Times-Roman) with sans-serif headings (Helvetica-Bold)
- Navy blue headings (#003366) for visual hierarchy
- Balanced margins (1.0 inch)
- Tight spacing to maximize content
- Small code font (8.5pt)

**Best for:**
- Engineering reports
- Scientific documentation
- Regulatory submissions
- Qualification reports (like ANSYS examples)

**Usage:**
```bash
pageforge document.md output.pdf --config examples/styles/technical-report.yaml
```

### Compact Dense Style (`compact-dense.yaml`)

Maximize content per page - good for reference documents.

**Characteristics:**
- Small fonts (9pt body, 8pt code)
- Minimal margins (0.75 inches)
- Very tight line spacing (1.1)
- Minimal paragraph spacing
- Sans-serif throughout

**Best for:**
- Reference manuals
- API documentation
- Quick reference guides
- Documents where content density is critical

**Usage:**
```bash
pageforge document.md output.pdf --config examples/styles/compact-dense.yaml
```

## Customizing Styles

Any of these styles can be customized further:

1. **Copy the style file:**
   ```bash
   cp examples/styles/latex-style.yaml my-custom-style.yaml
   ```

2. **Edit values** in `my-custom-style.yaml`

3. **Use your custom style:**
   ```bash
   pageforge document.md output.pdf --config my-custom-style.yaml
   ```

## Style Comparison

Generate the same document with different styles to compare:

```bash
# Generate with all styles
for style in examples/styles/*.yaml; do
    name=$(basename "$style" .yaml)
    pageforge examples/ANSYS_FDA_CSA_Roadmap.md "output-${name}.pdf" --config "$style"
done
```

## Font Reference

PageForge uses ReportLab's standard fonts:

**Serif fonts:**
- `Times-Roman`, `Times-Bold`, `Times-Italic`, `Times-BoldItalic`

**Sans-serif fonts:**
- `Helvetica`, `Helvetica-Bold`, `Helvetica-Oblique`, `Helvetica-BoldOblique`

**Monospace fonts:**
- `Courier`, `Courier-Bold`, `Courier-Oblique`, `Courier-BoldOblique`

## Creating Your Own Style

Start with the style closest to your needs and modify these key elements:

### 1. Margins
- **Generous margins (1.25"+):** Traditional, print-focused
- **Standard margins (1.0"):** Balanced
- **Tight margins (0.75"):** Maximize content

### 2. Line Spacing
- **Loose (1.5-1.6):** Easy reading, lots of whitespace
- **Normal (1.2-1.4):** Balanced
- **Tight (1.0-1.15):** Dense, fit more content

### 3. Font Combinations
- **Serif + Serif:** Traditional (Times throughout)
- **Sans + Sans:** Modern (Helvetica throughout)
- **Serif + Sans:** Professional (Times body + Helvetica headings)

### 4. Colors
- **Black text (#000000):** Traditional, high contrast
- **Dark gray (#2c3e50):** Modern, easier on eyes for screen reading
- **Colored headings:** Add visual hierarchy without being distracting

## Two-Column Layout

**Note:** Two-column magazine-style layout is not currently supported by PageForge. This would require significant changes to the PDF generation code.

**Workaround options:**
1. Use landscape orientation with narrower page width
2. Generate single-column PDF and post-process with external tools
3. Future enhancement: could add two-column support using ReportLab's `Frame` system

**If two-column layout is important for your use case, let us know and we can prioritize this feature.**

## Style Tips

### For Screen Reading
- Use `modern-minimal.yaml` with generous spacing
- Consider dark-gray text instead of pure black
- Larger fonts (11pt+ body)

### For Printing
- Use `latex-style.yaml` or `technical-report.yaml`
- Serif fonts are more readable on paper
- Tighter spacing is acceptable

### For Maximum Content
- Use `compact-dense.yaml`
- Consider landscape orientation for wide tables
- Test readability - don't go too small

### For Professional Reports
- Use `technical-report.yaml`
- Add colored headings for hierarchy
- Balance content density with whitespace

## Examples

See the `examples/` directory for sample documents. Try converting them with different styles to see the effects.
