"""Print PDF files to printer."""

import sys
import subprocess

import click

from angelflix.common import collect_pdfs

PRINTER_NAME = "LaserJet"
PRINT_OPTIONS = ["-o", "media=A4", "-o", "fit-to-page", "-o", "Duplex=DuplexNoTumble"]


def check_printer_exists(name):
    """Check if the specified printer is available."""
    try:
        output = subprocess.check_output(["lpstat", "-d", "-a"], text=True)
        available_printers = [line.split()[0] for line in output.strip().splitlines()]
        if name not in available_printers:
            click.echo(f"[ERROR] Printer '{name}' not found. Available printers:", err=True)
            for printer in available_printers:
                click.echo(f" - {printer}", err=True)
            return False
        return True
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Failed to check printers: {e}", err=True)
        return False


def print_file(filepath):
    """Send a single file to the printer."""
    try:
        result = subprocess.run(
            ["lp", "-d", PRINTER_NAME] + PRINT_OPTIONS + [str(filepath)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        click.echo(f"[OK] Printed: {filepath}")
    except Exception as e:
        click.echo(f"[ERROR] Failed to print '{filepath}': {e}", err=True)


@click.command("print")
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
def print_cmd(paths):
    """Print PDF files to the configured printer.

    PATHS can be PDF files or folders containing PDFs.
    """
    if not check_printer_exists(PRINTER_NAME):
        sys.exit(1)

    pdfs = collect_pdfs(paths)

    if not pdfs:
        click.echo("No PDF files found in the provided paths", err=True)
        sys.exit(1)

    for pdf_path in pdfs:
        print_file(pdf_path)
