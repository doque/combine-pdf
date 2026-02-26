"""Shared utilities for angelflix commands."""

import os
import sys
from pathlib import Path


def is_interactive():
    """Return True if stdout is a TTY (interactive terminal)."""
    return sys.stdout.isatty()


def collect_pdfs(paths):
    """
    Collect PDF files from a list of paths (files or folders).

    Args:
        paths: List of file paths or folder paths

    Returns:
        List of resolved Path objects to PDF files
    """
    pdfs = []
    for path in paths:
        p = Path(path).expanduser().resolve()
        if p.is_file():
            if p.suffix.lower() == ".pdf":
                pdfs.append(p)
            else:
                print(f"Skipping '{path}': Not a PDF file", file=sys.stderr)
        elif p.is_dir():
            for pdf in sorted(p.glob("*.pdf")):
                if pdf.is_file():
                    pdfs.append(pdf)
        else:
            print(f"Skipping '{path}': Does not exist", file=sys.stderr)
    return pdfs
