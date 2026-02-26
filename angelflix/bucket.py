"""Bucket PDF files by first letter into subdirectories."""

import sys
import shutil
from pathlib import Path
from collections import defaultdict

import click


def bucket_pdfs_in_folder(folder_path):
    """Bucket PDFs in a single folder by their first letter."""
    folder_path = Path(folder_path).resolve()
    if not folder_path.exists() or not folder_path.is_dir():
        click.echo(f"[WARNING] Skipping invalid folder: {folder_path}", err=True)
        return

    click.echo(f"[INFO] Processing folder: {folder_path}")
    all_pdfs = sorted([f for f in folder_path.glob("*.pdf") if f.is_file()])
    if not all_pdfs:
        click.echo("[INFO] No PDF files found.")
        return

    # Group files by their first letter (uppercased), fallback to '#'
    buckets = defaultdict(list)
    for pdf in all_pdfs:
        first_char = pdf.name[0].upper()
        if not first_char.isalpha():
            first_char = "#"
        buckets[first_char].append(pdf)

    # Create one folder per letter group
    for letter, files in sorted(buckets.items()):
        bucket_dir = folder_path / letter
        bucket_dir.mkdir(exist_ok=True)

        for f in files:
            target = bucket_dir / f.name
            click.echo(f"Moving {f.name} -> {letter}/")
            shutil.move(str(f), target)

    click.echo(f"[DONE] Bucketing complete for {folder_path}\n")


@click.command()
@click.argument("folders", nargs=-1, required=True)
def bucket(folders):
    """Bucket PDF files by first letter into subdirectories.

    FOLDERS should be directories containing PDF files to organize.
    """
    for folder in folders:
        bucket_pdfs_in_folder(folder)
