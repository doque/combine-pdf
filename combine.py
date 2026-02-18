#!/usr/bin/env python3
import os
import sys
import shutil
import fitz  # PyMuPDF


def process_pdf(filepath):
    """Process a single PDF file and return output path if successful."""
    base, ext = os.path.splitext(filepath)
    if ext.lower() != ".pdf":
        return None

    doc = fitz.open(filepath)
    new_doc = fitz.open()

    if len(doc) >= 1:
        new_doc.insert_pdf(doc, from_page=0, to_page=0)

    if len(doc) >= 3:
        w, h = doc[1].rect.width, doc[1].rect.height
        new_page = new_doc.new_page(width=w * 2, height=h)
        new_page.show_pdf_page(fitz.Rect(0, 0, w, h), doc, 1)
        new_page.show_pdf_page(fitz.Rect(w, 0, w * 2, h), doc, 2)

    output_file = f"{base}_output.pdf"
    new_doc.save(output_file)
    new_doc.close()
    doc.close()
    print(f"Created: {output_file}")
    return output_file


def collect_pdfs_from_path(path):
    """Return list of PDF files from a path (file or folder)."""
    pdfs = []
    if os.path.isfile(path):
        if path.lower().endswith(".pdf"):
            pdfs.append(path)
        else:
            print(f"Skipping '{path}': Not a PDF file")
    elif os.path.isdir(path):
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path) and file.lower().endswith(".pdf"):
                pdfs.append(full_path)
    else:
        print(f"Skipping '{path}': Does not exist")
    return pdfs


def main():
    if len(sys.argv) < 2:
        print("Usage: combine-pdf <file|folder> [file|folder ...]")
        print("  Accepts any combination of PDF files and folders containing PDFs")
        sys.exit(1)

    # Collect all PDF files from arguments
    all_pdfs = []
    input_paths = sys.argv[1:]

    for path in input_paths:
        all_pdfs.extend(collect_pdfs_from_path(path))

    if not all_pdfs:
        print("No PDF files found in the provided paths")
        sys.exit(1)

    print(f"Found {len(all_pdfs)} PDF file(s) to process\n")

    # Process each PDF
    processed_files = []
    for pdf_path in all_pdfs:
        result = process_pdf(pdf_path)
        if result:
            processed_files.append(pdf_path)

    if not processed_files:
        print("\nNo files were processed")
        sys.exit(0)

    print(f"\nProcessed {len(processed_files)} file(s)")

    # Prompt for cleanup
    response = input("\nRemove original files? [y/N]: ").strip().lower()
    if response == "y":
        # Track folders to potentially remove
        folders_to_check = set()

        for pdf_path in processed_files:
            parent = os.path.dirname(pdf_path)
            if parent and parent in input_paths:
                folders_to_check.add(parent)
            try:
                os.remove(pdf_path)
                print(f"Removed: {pdf_path}")
            except OSError as e:
                print(f"Failed to remove {pdf_path}: {e}")

        # Check if any input folders are now empty and offer to remove them
        empty_folders = [f for f in folders_to_check if os.path.isdir(f) and not os.listdir(f)]
        if empty_folders:
            response = input(f"\nRemove {len(empty_folders)} empty folder(s)? [y/N]: ").strip().lower()
            if response == "y":
                for folder in empty_folders:
                    try:
                        shutil.rmtree(folder)
                        print(f"Removed folder: {folder}")
                    except OSError as e:
                        print(f"Failed to remove {folder}: {e}")


if __name__ == "__main__":
    main()
