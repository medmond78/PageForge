---
title: PageForge Feature Test Document
author: PageForge Test Suite
date: 2026-08-12
description: Comprehensive test document covering all supported markdown features
---

# Level 1 Heading: Introduction

This is a comprehensive test document designed to verify all supported markdown features in PageForge. It includes **bold text**, *italic text*, and `inline code` formatting within paragraphs.

This paragraph demonstrates inline styling: **bold**, *italic*, ***bold italic***, and `code`. You can also combine them: ***bold italic with `code` inside***.

## Level 2 Heading: Text Formatting

### Level 3 Heading: Inline Elements

Here we test various inline formatting options:

- **Bold text** using double asterisks
- *Italic text* using single asterisks
- `Inline code` using backticks
- Combined: ***bold and italic*** text

#### Level 4 Heading: Nested Content

This section contains multiple levels of headings to verify proper hierarchy and styling.

##### Level 5 Heading: Deep Nesting

Even deeper content to test heading size progression.

###### Level 6 Heading: Deepest Level

The smallest heading level supported by markdown.

## Level 2 Heading: Lists

### Unordered Lists

Simple unordered list:

- First item
- Second item
- Third item

Nested unordered list:

- Top level item 1
  - Nested item 1.1
  - Nested item 1.2
    - Deep nested item 1.2.1
    - Deep nested item 1.2.2
  - Nested item 1.3
- Top level item 2
  - Nested item 2.1
- Top level item 3

### Ordered Lists

Simple ordered list:

1. First numbered item
2. Second numbered item
3. Third numbered item

Nested ordered list:

1. Top level item 1
   1. Nested item 1.1
   2. Nested item 1.2
      1. Deep nested item 1.2.1
      2. Deep nested item 1.2.2
   3. Nested item 1.3
2. Top level item 2
   1. Nested item 2.1
   2. Nested item 2.2
3. Top level item 3

### Mixed Lists

You can also mix ordered and unordered lists:

1. Ordered item 1
   - Unordered nested 1.1
   - Unordered nested 1.2
2. Ordered item 2
   - Unordered nested 2.1
     1. Ordered deep nested 2.1.1
     2. Ordered deep nested 2.1.2

## Level 2 Heading: Code Blocks

### Python Code

Here's a Python code block with syntax highlighting:

```python
def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

### JavaScript Code

And here's a JavaScript example:

```javascript
// Function to calculate factorial
function factorial(n) {
  if (n <= 1) {
    return 1;
  }
  return n * factorial(n - 1);
}

// Arrow function example
const square = (x) => x * x;

// Test the functions
console.log("5! =", factorial(5));
console.log("4^2 =", square(4));
```

### Plain Code Block

Code without language specification:

```
This is a plain code block
without syntax highlighting.
It preserves formatting:
  - indentation
  - spacing
  - special characters: <>&
```

## Level 2 Heading: Blockquotes

> This is a blockquote.
> It can span multiple lines.
> And it maintains formatting.

> Blockquotes can also contain **bold** and *italic* text.
>
> They can have multiple paragraphs too.

Nested blockquotes:

> This is the outer quote.
>
> > This is a nested quote.
> >
> > > And this is even more nested.

## Level 2 Heading: Horizontal Rules

Horizontal rules can be created with three or more hyphens:

---

Or with three or more asterisks:

***

They help separate sections of content.

---

## Level 2 Heading: Images

### PNG Images

Here's a PNG image:

![Test PNG Image](test-image.png)

### SVG Images

And here's an SVG diagram:

![Test SVG Diagram](test-diagram.svg)

### Multiple Images

You can include multiple images in a document:

![Test Image 1](test-image.png)

![Test Diagram](test-diagram.svg)

## Level 2 Heading: Tables

Tables are supported via the markdown extra extension:

| Feature | Status | Priority |
|---------|--------|----------|
| Bold text | Complete | High |
| Italic text | Complete | High |
| Code blocks | Complete | High |
| Tables | Complete | Medium |
| Images | Complete | High |

More complex table with alignment:

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left 1 | Center 1 | Right 1 |
| Left 2 | Center 2 | Right 2 |
| Left 3 | Center 3 | Right 3 |

Table with longer content:

| Component | Description | Implementation Status |
|-----------|-------------|----------------------|
| Parser | Converts Markdown to structured format | Complete |
| Generator | Generates PDF from parsed content | Complete |
| Image Handler | Resolves and embeds images | Complete |
| Style System | Applies formatting to elements | Complete |

## Level 2 Heading: Complex Combinations

### Code in Lists

Lists can contain code blocks:

1. First step: Install the package
   ```bash
   pip install pageforge
   ```

2. Second step: Create a markdown file
   ```markdown
   # My Document
   This is content.
   ```

3. Third step: Convert to PDF
   ```bash
   pageforge input.md output.pdf
   ```

### Lists with Inline Code

- Use `pageforge input.md` to convert with default settings
- Use `pageforge input.md output.pdf --config config.yaml` for custom config
- Use `pageforge --help` to see all options

### Blockquotes with Code

> To install PageForge, run:
>
> ```bash
> pip install pageforge
> ```
>
> Then you can start converting markdown files to PDF.

## Level 2 Heading: Special Characters

Testing special characters and escaping:

- Angle brackets: < and >
- Ampersand: &
- Quotes: "double" and 'single'
- Apostrophes: don't, won't, can't
- Em dash — and en dash –
- Ellipsis...

## Level 2 Heading: Long Paragraphs

This is a longer paragraph to test text wrapping and flow. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

Another long paragraph follows. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.

## Level 2 Heading: Conclusion

This document has demonstrated all major markdown features supported by PageForge:

1. **Headings**: All six levels (H1-H6)
2. **Text formatting**: Bold, italic, and inline code
3. **Lists**: Ordered, unordered, and nested combinations
4. **Code blocks**: With and without syntax highlighting
5. **Blockquotes**: Including nested blockquotes
6. **Horizontal rules**: Section separators
7. **Images**: PNG and SVG formats
8. **Tables**: With various alignments and content
9. **Special characters**: Proper escaping and rendering

---

**End of test document**
