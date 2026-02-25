# combine-pdf

Combine PDF pages side-by-side for 2-up A4 printing. Optimized for saving paper.

## How it works

- **Odd page count** (e.g., 3 pages): Page 1 stays full A4 portrait, remaining pages paired side-by-side (2+3, 4+5, etc.)
- **Even page count** (e.g., 4 pages): All pages paired from start (1+2, 3+4, etc.)

Output is A4 landscape with each source page scaled to A5.

## Installation

```bash
pip install -e .
```

This installs the `combine-pdf` command globally.

## Usage

```bash
combine-pdf document.pdf
combine-pdf doc1.pdf doc2.pdf folder/
combine-pdf --help
```

After processing, you'll be prompted whether to remove the original files.
