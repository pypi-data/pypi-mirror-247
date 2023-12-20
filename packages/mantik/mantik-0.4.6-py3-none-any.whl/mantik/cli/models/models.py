import json
import typing as t
import uuid

import click

import mantik.authentication.auth
import mantik.cli.main as main
import mantik.utils.env
import mantik.utils.mantik_api.client
import mantik.utils.mantik_api.models

GROUP_NAME = "models"
_PROJECT_ID_ENV_VAR = "MANTIK_PROJECT_ID"
_MODEL_ID_ENV_VAR = "MANTIK_MODEL_ID"


def _access_token_from_env_vars() -> str:
    return mantik.authentication.auth.get_valid_access_token()


@main.cli.group(GROUP_NAME)
def cli() -> None:
    """Interaction with models through the mantik api."""


def mlflow_parameters_decoder(ctx, param, value) -> t.Optional[dict]:
    try:
        return json.loads(value) if value is not None else None
    except json.decoder.JSONDecodeError:
        raise TypeError(
            """MLflow parameters are in the wrong format. Try: '{"key": "value"}'"""  # noqa
        )


@cli.command("list")
@click.option(
    "--project-id",
    type=uuid.UUID,
    required=True,
    envvar=_PROJECT_ID_ENV_VAR,
)
def get_all_project_models(project_id: uuid.UUID) -> None:
    """Print details of all trained models in project."""
    models = mantik.utils.mantik_api.models.get_all(
        project_id=project_id,
        token=_access_token_from_env_vars(),
    )
    click.echo(models)


@cli.command("get-one")
@click.option(
    "--project-id",
    type=uuid.UUID,
    required=True,
    envvar=_PROJECT_ID_ENV_VAR,
)
@click.option(
    "--model-id", type=uuid.UUID, required=True, envvar=_MODEL_ID_ENV_VAR
)
def get_model(project_id: uuid.UUID, model_id: uuid.UUID) -> None:
    """Print details of specific trained model."""

    model = mantik.utils.mantik_api.models.get_one(
        project_id=project_id,
        model_id=model_id,
        token=_access_token_from_env_vars(),
    )
    click.echo(model)


@cli.command("delete")
@click.option(
    "--project-id",
    type=uuid.UUID,
    required=True,
    envvar=_PROJECT_ID_ENV_VAR,
)
@click.option(
    "--model-id", type=uuid.UUID, required=True, envvar=_MODEL_ID_ENV_VAR
)
def delete_model(project_id: uuid.UUID, model_id: uuid.UUID) -> None:
    """Delete a trained model."""
    mantik.utils.mantik_api.models.delete(
        project_id=project_id,
        model_id=model_id,
        token=_access_token_from_env_vars(),
    )


@cli.command("add")
@click.option(
    "--project-id",
    type=uuid.UUID,
    required=True,
    envvar=_PROJECT_ID_ENV_VAR,
)
@click.option("--uri", type=str, required=True)
@click.option("--location", type=str, required=True)
@click.option("--connection-id", type=uuid.UUID, required=False)
@click.option(
    "--mlflow-parameters",
    type=str,
    required=False,
    help="""JSON data as a string.""",
    callback=mlflow_parameters_decoder,
)
@click.option("--model-repository-id", type=uuid.UUID, required=False)
def create_model_entry(
    project_id: uuid.UUID,
    uri: str,
    location: str,
    connection_id: t.Optional[uuid.UUID],
    mlflow_parameters: t.Optional[dict],
    model_repository_id: t.Optional[uuid.UUID],
) -> None:
    """Add a new trained model entry."""

    mantik.utils.mantik_api.models.add(
        project_id=project_id,
        new_model_schema=mantik.utils.mantik_api.models.PostPutModel(
            uri=uri,
            location=location,
            connection_id=connection_id,
            mlflow_parameters=mlflow_parameters,
            model_repository_id=model_repository_id,
        ),
        token=_access_token_from_env_vars(),
    )


@cli.command("update")
@click.option(
    "--project-id",
    type=uuid.UUID,
    required=True,
    envvar=_PROJECT_ID_ENV_VAR,
)
@click.option(
    "--model-id", type=uuid.UUID, required=True, envvar=_MODEL_ID_ENV_VAR
)
@click.option("--uri", type=str, required=True)
@click.option("--location", type=str, required=True)
@click.option("--connection-id", type=uuid.UUID, required=False)
@click.option(
    "--mlflow-parameters",
    type=str,
    required=False,
    help="""JSON data as a string.""",
    callback=mlflow_parameters_decoder,
)
@click.option("--model-repository-id", type=uuid.UUID, required=False)
def update_model_entry(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    uri: str,
    location: str,
    connection_id: t.Optional[uuid.UUID],
    mlflow_parameters: t.Optional[dict],
    model_repository_id: t.Optional[uuid.UUID],
) -> None:
    """Update details of existing trained model."""

    mantik.utils.mantik_api.models.update(
        project_id=project_id,
        model_id=model_id,
        updated_model_schema=mantik.utils.mantik_api.models.PostPutModel(
            uri=uri,
            location=location,
            connection_id=connection_id,
            mlflow_parameters=mlflow_parameters,
            model_repository_id=model_repository_id,
        ),
        token=_access_token_from_env_vars(),
    )
