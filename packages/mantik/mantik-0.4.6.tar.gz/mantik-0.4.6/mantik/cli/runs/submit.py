import logging
import pathlib
import typing as t
import uuid

import click

import mantik
import mantik.cli._options as _main_options
import mantik.cli.runs.runs as runs
import mantik.cli.utils as cli_utils
import mantik.compute_backend.config.core as core
import mantik.compute_backend.config.read as read
import mantik.utils.env_vars as env_vars
import mantik.utils.mantik_api as mantik_api

logger = logging.getLogger(__name__)


@runs.cli.command("submit")
@click.argument(
    "mlproject-path",
    type=click.Path(path_type=pathlib.Path),
    required=True,
)
@click.option(
    "--run-name",
    default=None,
    type=str,
    help="Name of the Run.",
    required=True,
)
@click.option(
    "--entry-point",
    required=False,
    default="main",
    show_default=True,
    help="Entrypoint of the MLproject file.",
)
@click.option(
    "--backend-config",
    type=click.Path(dir_okay=False, path_type=pathlib.Path),
    required=True,
    help="Relative or absolute path to backend config file.",
)
@click.option(
    "--project-id",
    type=uuid.UUID,
    default=None,
    help=f"""Project ID on Mantik.

        If not specified, it is inferred from the environment variable
        {env_vars._PROJECT_ID_ENV_VAR}.

    """,
)
@click.option(
    "--data-repository-id",
    type=uuid.UUID,
    default=None,
    help=f"""Data repository ID on Mantik

        If not specified, it is inferred from the environment variable
        {env_vars._DATA_REPOSITORY_ID_ENV_VAR}.

    """,
)
@click.option(
    "--experiment-repository-id",
    type=uuid.UUID,
    default=None,
    help=f"""Experiment repository ID on Mantik

        If not specified, it is inferred from the environment variable
        {env_vars._EXPERIMENT_REPOSITORY_ID_ENV_VAR}.

    """,
)
@click.option(
    "--code-repository-id",
    type=uuid.UUID,
    default=None,
    help=f"""Code repository ID on Mantik

        If not specified, it is inferred from the environment variable
        {env_vars._CODE_REPOSITORY_ID_ENV_VAR}.

    """,
)
@click.option(
    "--branch",
    default=None,
    type=str,
    help="Name of the code repository's branch you want to use for this run",
    required=True,
)
@click.option(
    "--commit",
    default=None,
    type=str,
    help="""Name of the code repository's full commit hash you want to use for
        this run.

        If both branch and commit hash are given, the commit hash is preferred
        over the branch.
    """,
    required=False,
)
@click.option(
    "--compute-budget-account",
    type=str,
    default=None,
    help=f"""Name of your Compute Budget Account on HPC

        If not specified, it is inferred from the environment variable
        {core._PROJECT_ENV_VAR}.

    """,
)
@click.option(
    "--parameter", "-P", show_default=True, default=lambda: [], multiple=True
)
@_main_options.VERBOSE
@click.option(
    "--connection-id",
    required=True,
    default=None,
    type=uuid.UUID,
    help="Connection ID of your UNICORE Connection stored on Mantik. "
    "This is preferred over using env vars.",
)
def run_project(
    run_name: str,
    mlproject_path: pathlib.Path,
    entry_point: str,
    backend_config: pathlib.Path,
    parameter: t.List[str],
    verbose: bool,  # noqa
    project_id: t.Optional[uuid.UUID],
    data_repository_id: t.Optional[uuid.UUID],
    experiment_repository_id: t.Optional[uuid.UUID],
    code_repository_id: t.Optional[uuid.UUID],
    branch: t.Optional[str],
    commit: t.Optional[str],
    compute_budget_account: t.Optional[str],
    connection_id: t.Optional[uuid.UUID],
) -> None:
    """Submit an MLflow project as a run to the Mantik Compute Backend.

    Note that `MLPROJECT_PATH` is the relative path to the MLflow project
    folder with your Code Repository as root.

    Remember that when you submit a run, the code is retrieved from your
    remote Git Code Repository. So make sure to commit and push your
    changes before submitting a run! The only file read from your local
    system is the backend config.

    To find the respective required IDs make sure to check Mantik's UI

    """
    entry_point = entry_point or "main"
    project_id = project_id or mantik.utils.env.get_required_env_var(
        env_vars._PROJECT_ID_ENV_VAR
    )
    data_repository_id = (
        data_repository_id
        or mantik.utils.env.get_optional_env_var(
            env_vars._DATA_REPOSITORY_ID_ENV_VAR
        )
    )
    experiment_repository_id = (
        experiment_repository_id
        or mantik.utils.env.get_required_env_var(
            env_vars._EXPERIMENT_REPOSITORY_ID_ENV_VAR
        )
    )
    code_repository_id = (
        code_repository_id
        or mantik.utils.env.get_required_env_var(
            env_vars._CODE_REPOSITORY_ID_ENV_VAR
        )
    )
    compute_budget_account = (
        compute_budget_account
        or mantik.utils.env.get_required_env_var(core._PROJECT_ENV_VAR)
    )
    if branch is None and commit is None:
        raise ValueError(
            "Either provide a branch or full commit hash to submit"
        )
    elif branch is not None and commit is not None:
        logger.warning(
            "Both branch name %s and commit hash %s given, using commit hash to"
            " submit run",
            branch,
            commit,
        )

    logger.debug("Parsing MLflow entry point parameters")
    parameters = cli_utils.dict_from_list(parameter)

    config = read.read_config(backend_config)
    data = {
        "name": run_name,
        "experimentRepositoryId": str(experiment_repository_id),
        "codeRepositoryId": str(code_repository_id),
        "branch": branch,
        "commit": commit,
        "dataRepositoryId": str(data_repository_id)
        if data_repository_id is not None
        else None,
        "connectionId": str(connection_id),
        "computeBudgetAccount": compute_budget_account,
        "mlflowMlprojectFilePath": mlproject_path.as_posix(),
        "entryPoint": entry_point,
        "mlflowParameters": parameters,
        "backendConfig": config,
    }
    token = mantik.authentication.auth.get_valid_access_token()
    response = mantik_api.run.submit_run(
        project_id=project_id, submit_run_data=data, token=token
    )
    click.echo(response.content)
