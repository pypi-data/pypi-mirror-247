import uuid

import click

CONNECTION_ID = click.option(
    "--connection-id",
    required=False,
    default=None,
    type=uuid.UUID,
    help="Connection ID of your Connection stored on Mantik.",
)

DATA_REPOSITORY_NAME = click.option(
    "--name",
    required=False,
    default=None,
    type=str,
    help="Data repository name, displayed in Mantik. "
    "When not passed the TARGET is passed as name.",
)

DATA_REPOSITORY_ID = click.option(
    "--id",
    required=False,
    default=None,
    type=uuid.UUID,
    help="Data repository ID.",
)

DATA_REPOSITORY_DESCRIPTION = click.option(
    "--description",
    required=False,
    default=None,
    type=str,
    help="Data repository description, displayed in Mantik.",
)
