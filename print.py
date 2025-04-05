#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

PRINTER_NAME = "LaserJet"
PRINT_OPTIONS = ["-o", "media=A4", "-o", "fit-to-page", "-o", "Duplex=DuplexNoTumble"]

def check_printer_exists(name):
    try:
        output = subprocess.check_output(["lpstat", "-p"], text=True)
        return any(name in line for line in output.splitlines())
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to check printers: {e}")
        return False

def print_file(filepath):
    try:
        result = subprocess.run(
            ["lp", "-d", PRINTER_NAME] + PRINT_OPTIONS + [str(filepath)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        else:
            print(f"[OK] Sent to printer: {filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to print '{filepath}': {e}")

def main(folders):
    if not check_printer_exists(PRINTER_NAME):
        print(f"[ERROR] Printer '{PRINTER_NAME}' not found. Exiting.")
        sys.exit(1)

    for folder in folders:
        folder_path = Path(folder).expanduser().resolve()
        if not folder_path.exists() or not folder_path.is_dir():
            print(f"[WARNING] Skipping invalid folder: {folder_path}")
            continue

        for pdf in folder_path.glob("*.pdf"):
            print_file(pdf)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python print.py folder1 [folder2 ...]")
        sys.exit(1)
    main(sys.argv[1:])
