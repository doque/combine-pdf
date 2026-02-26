# angelflix-scripts

PDF utilities for combining, printing, and organizing.

## Installation

```bash
pip install -e .
```

Installs the `angelflix` command globally.

## Commands

### combine

Combine PDF page pairs side-by-side on A4 landscape for 2-up printing.

```bash
angelflix combine document.pdf
angelflix combine doc1.pdf doc2.pdf folder/
```

- **Odd page count**: Page 1 stays full A4 portrait, rest paired (2+3, 4+5, etc.)
- **Even page count**: All pages paired from start (1+2, 3+4, etc.)
- **Interactive mode**: Creates `_output.pdf` files, prompts for cleanup
- **Piped mode**: Outputs combined PDF to stdout (`angelflix combine input.pdf > output.pdf`)

### print

Print PDF files to the configured LaserJet printer.

```bash
angelflix print document.pdf
angelflix print folder/
```

### bucket

Organize PDFs into subdirectories by first letter.

```bash
angelflix bucket folder/
```

Creates A/, B/, C/... subdirectories and moves PDFs accordingly.
