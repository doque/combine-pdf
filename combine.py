import os
import sys
import fitz  # PyMuPDF

def process_pdf(filepath):
    base, ext = os.path.splitext(filepath)
    if ext.lower() != ".pdf":
        return

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
    print(f"✅ Created: {output_file}")

# Check for folder arguments
if len(sys.argv) < 2:
    print("Usage: python combine.py folder1 [folder2 ...]")
    sys.exit(1)

# Process each folder
for folder in sys.argv[1:]:
    if not os.path.isdir(folder):
        print(f"⚠️ Skipping '{folder}': Not a folder")
        continue

    for file in os.listdir(folder):
        full_path = os.path.join(folder, file)
        if os.path.isfile(full_path) and file.lower().endswith(".pdf"):
            process_pdf(full_path)