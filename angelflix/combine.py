"""Combine PDF page pairs side-by-side on A4 landscape for 2-up printing."""

import os
import sys
import shutil

import click
import fitz  # PyMuPDF

from angelflix.common import collect_pdfs, is_interactive

# A4 dimensions in points (landscape for 2-up printing)
A4_WIDTH = 841.89
A4_HEIGHT = 595.28


def process_pdf(filepath):
    """Process a single PDF file, combining page pairs side-by-side on A4 landscape."""
    doc = fitz.open(filepath)
    new_doc = fitz.open()
    page_count = len(doc)

    # Odd pages: keep page 1 full, pair the rest
    # Even pages: pair all from the start
    if page_count % 2 == 1:
        # First page stays full A4 portrait
        new_doc.insert_pdf(doc, from_page=0, to_page=0)
        start_idx = 1
    else:
        start_idx = 0

    # Process remaining pages in pairs
    for i in range(start_idx, page_count, 2):
        # Create A4 landscape page
        new_page = new_doc.new_page(width=A4_WIDTH, height=A4_HEIGHT)
        half_width = A4_WIDTH / 2

        # Left page
        left_rect = fitz.Rect(0, 0, half_width, A4_HEIGHT)
        new_page.show_pdf_page(left_rect, doc, i)

        # Right page if it exists
        if i + 1 < page_count:
            right_rect = fitz.Rect(half_width, 0, A4_WIDTH, A4_HEIGHT)
            new_page.show_pdf_page(right_rect, doc, i + 1)

    output_bytes = new_doc.tobytes()
    output_pages = len(new_doc)
    new_doc.close()
    doc.close()
    return output_bytes, output_pages, page_count


@click.command()
@click.argument("paths", nargs=-1, required=True)
def combine(paths):
    """Combine PDF page pairs side-by-side on A4 landscape.

    PATHS can be PDF files or folders containing PDFs.

    When piped (not interactive), outputs combined PDF to stdout.
    When interactive, creates _output.pdf files and offers cleanup.
    """
    pdfs = collect_pdfs(paths)

    if not pdfs:
        click.echo("No PDF files found in the provided paths", err=True)
        sys.exit(1)

    if is_interactive():
        # Interactive mode: write individual output files
        click.echo(f"Found {len(pdfs)} PDF file(s) to process\n")
        processed_files = []

        for pdf_path in pdfs:
            output_bytes, output_pages, original_pages = process_pdf(pdf_path)
            base = os.path.splitext(pdf_path)[0]
            output_file = f"{base}_output.pdf"
            with open(output_file, "wb") as f:
                f.write(output_bytes)
            click.echo(f"Created: {output_file} ({output_pages} pages from {original_pages} originals)")
            processed_files.append(pdf_path)

        if not processed_files:
            click.echo("\nNo files were processed")
            sys.exit(0)

        click.echo(f"\nProcessed {len(processed_files)} file(s)")

        # Prompt for cleanup
        if click.confirm("\nRemove original files?", default=False):
            input_paths = set(paths)
            folders_to_check = set()

            for pdf_path in processed_files:
                parent = os.path.dirname(pdf_path)
                if parent and parent in input_paths:
                    folders_to_check.add(parent)
                try:
                    os.remove(pdf_path)
                    click.echo(f"Removed: {pdf_path}")
                except OSError as e:
                    click.echo(f"Failed to remove {pdf_path}: {e}", err=True)

            # Check for empty folders
            empty_folders = [f for f in folders_to_check if os.path.isdir(f) and not os.listdir(f)]
            if empty_folders and click.confirm(f"\nRemove {len(empty_folders)} empty folder(s)?", default=False):
                for folder in empty_folders:
                    try:
                        shutil.rmtree(folder)
                        click.echo(f"Removed folder: {folder}")
                    except OSError as e:
                        click.echo(f"Failed to remove {folder}: {e}", err=True)
    else:
        # Piped mode: concatenate all into single PDF, output to stdout
        combined_doc = fitz.open()

        for pdf_path in pdfs:
            output_bytes, _, _ = process_pdf(pdf_path)
            temp_doc = fitz.open("pdf", output_bytes)
            combined_doc.insert_pdf(temp_doc)
            temp_doc.close()

        sys.stdout.buffer.write(combined_doc.tobytes())
        combined_doc.close()
