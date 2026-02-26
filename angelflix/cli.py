"""Main CLI entry point for angelflix."""

import click

from angelflix.combine import combine
from angelflix.print_ import print_cmd
from angelflix.bucket import bucket


@click.group()
@click.version_option(version="1.0.0", prog_name="angelflix")
def main():
    """Angelflix PDF utilities."""
    pass


main.add_command(combine)
main.add_command(print_cmd, name="print")
main.add_command(bucket)


if __name__ == "__main__":
    main()
