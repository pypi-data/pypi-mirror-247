import click

SOURCE = click.argument(
    "source",
    type=str,
    nargs=1,
    required=True,
)
TARGET = click.argument(
    "target",
    type=str,
    nargs=1,
    required=True,
)
