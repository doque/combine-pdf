#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

PRINTER_NAME = "LaserJet"
PRINT_OPTIONS = ["-o", "media=A4", "-o", "fit-to-page", "-o", "Duplex=DuplexNoTumble"]

def check_printer_exists(name):
    try:
        output = subprocess.check_output(["lpstat", "-d", "-a"], text=True)
        available_printers = [line.split()[0] for line in output.strip().splitlines()]
        if name not in available_printers:
            print(f"[ERROR] Printer '{name}' not found. Available printers:")
            for printer in available_printers:
                print(f" - {printer}")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to check printers: {e}")
        return False

def print_file(filepath):
    try:
        full_path = Path(filepath).resolve(strict=True)
        result = subprocess.run(
            ["lp", "-d", PRINTER_NAME] + PRINT_OPTIONS + [str(full_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        else:
            print(f"[OK] Printed: {full_path}")
    except Exception as e:
        print(f"[ERROR] Failed to print '{filepath}': {e}")

def main(paths):
    if not check_printer_exists(PRINTER_NAME):
        sys.exit(1)

    for path in paths:
        item = Path(path).expanduser().resolve()
        if not item.exists():
            print(f"[WARNING] Skipping non-existent path: {item}")
            continue

        if item.is_file() and item.suffix.lower() == ".pdf":
            print_file(item)
        elif item.is_dir():
            for pdf in sorted(item.glob("*.pdf")):
                print_file(pdf)
        else:
            print(f"[WARNING] Skipping unsupported item: {item}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python print.py file_or_folder1 [file_or_folder2 ...]")
        sys.exit(1)
    main(sys.argv[1:])