# combine-pdf

Combine PDF pages into a single document. Takes the first page as-is, then combines pages 2-3 side by side.

## Installation

```bash
pip install -e .
```

This installs the `combine-pdf` command globally.

## Usage

```bash
# Single file
combine-pdf document.pdf

# Multiple files
combine-pdf doc1.pdf doc2.pdf doc3.pdf

# Single folder (processes all PDFs inside)
combine-pdf my_folder

# Multiple folders
combine-pdf folder1 folder2

# Mix of files and folders
combine-pdf doc1.pdf my_folder doc2.pdf another_folder
```

After processing, you'll be prompted whether to remove the original files.
