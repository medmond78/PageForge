# Spacing Configuration Fix

## Problems Found

All 5 style configuration files had **incorrect YAML key names** for spacing, causing spacing settings to be completely ignored and fall back to hardcoded defaults.

### Wrong Keys Used (Not Loaded)

```yaml
spacing:
  line_spacing: 1.1          # ❌ Wrong key
  paragraph_spacing: 6       # ❌ Wrong key  
  heading_spacing: 10        # ❌ Wrong key (and incomplete)
  list_indent: 20            # ✅ Correct
```

### Correct Keys (Now Fixed)

```yaml
spacing:
  line_height: 1.1           # ✅ Line spacing multiplier
  paragraph: 6               # ✅ Points after paragraphs
  heading_before: 10         # ✅ Points before headings
  heading_after: 4           # ✅ Points after headings
  list_indent: 20            # ✅ List indentation
```

## What This Caused

**Before fix:**
- All spacing settings in style YAMLs were **completely ignored**
- Fell back to defaults from `config.py`:
  - `paragraph: 12` (instead of configured 6 for academic)
  - `heading_before: 18` (instead of configured 10)
  - `heading_after: 6` (instead of configured 4)
  - `line_height: 1.2` (instead of configured 1.1)

**Result:** PDFs had **uneven spacing** - too much space between paragraphs and around headings, looser line spacing than intended.

## How Spacing Works in PageForge

### 1. Line Height (`line_height`)

Controls spacing between lines within a paragraph.

- **Value:** Multiplier (1.0 = single spacing, 1.5 = 1.5x spacing)
- **Academic papers:** 1.0-1.1 (very tight)
- **Normal documents:** 1.2-1.4
- **Loose/readable:** 1.5-1.6

**Example:**
```yaml
line_height: 1.1  # Tight academic spacing
```

### 2. Paragraph Spacing (`paragraph`)

Space added **after** each paragraph (in points).

- **Academic papers:** 4-6 points (minimal)
- **Normal documents:** 8-12 points
- **Loose layouts:** 12-18 points

**Example:**
```yaml
paragraph: 6  # Minimal space after paragraphs
```

### 3. Heading Spacing (`heading_before`, `heading_after`)

Space added **before** and **after** each heading (in points).

- `heading_before`: Creates visual break before section
- `heading_after`: Small space before content starts

**Academic papers:**
```yaml
heading_before: 10  # Moderate break before section
heading_after: 4    # Small gap after heading
```

**Readable documents:**
```yaml
heading_before: 18  # Larger break for emphasis
heading_after: 6    # More breathing room
```

### 4. List Indentation (`list_indent`)

How far list items are indented from the left margin (in points).

**Example:**
```yaml
list_indent: 20  # Standard indentation
```

## All Fixed Files

1. `academic-journal.yaml`
2. `latex-style.yaml`
3. `technical-report.yaml`
4. `modern-minimal.yaml`
5. `compact-dense.yaml`

## Testing

Generate a PDF with the fixed spacing:

```bash
pageforge document.md output.pdf --config examples/styles/academic-journal.yaml
```

Compare before and after:
- **Before:** Loose spacing, uneven gaps
- **After:** Tight, consistent academic spacing

## Reference

See `examples/pageforge.yaml` for the canonical example with correct key names and detailed comments.
