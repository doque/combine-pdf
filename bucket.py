#!/usr/bin/env python3

import sys
import shutil
from pathlib import Path
from collections import defaultdict

def bucket_pdfs_in_folder(folder_path: Path):
    folder_path = folder_path.resolve()
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"[WARNING] Skipping invalid folder: {folder_path}")
        return

    print(f"[INFO] Processing folder: {folder_path}")
    all_pdfs = sorted([f for f in folder_path.glob("*.pdf") if f.is_file()])
    if not all_pdfs:
        print("[INFO] No PDF files found.")
        return

    # Group files by their first letter (uppercased), fallback to '#'
    buckets = defaultdict(list)
    for pdf in all_pdfs:
        first_char = pdf.name[0].upper()
        if not first_char.isalpha():
            first_char = "#"  # Non-letter start
        buckets[first_char].append(pdf)

    # Create one folder per letter group or combination
    for letter, files in sorted(buckets.items()):
        bucket_name = letter  # Use A, B, C, ..., or '#'
        bucket_dir = folder_path / bucket_name
        bucket_dir.mkdir(exist_ok=True)

        for f in files:
            target = bucket_dir / f.name
            print(f"Moving {f.name} → {bucket_name}/")
            shutil.move(str(f), target)

    print(f"[DONE] Bucketing complete for {folder_path}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python bucket.py folder1 [folder2 ...]")
        sys.exit(1)

    for folder_arg in sys.argv[1:]:
        bucket_pdfs_in_folder(Path(folder_arg))

if __name__ == "__main__":
    main()