import logging
import pathlib
import platform
import typing as t
import uuid

import click

import mantik
import mantik.cli._options as _main_options
import mantik.cli.runs.runs as runs
import mantik.cli.utils as cli_utils
import mantik.runs.local as local_runs
import mantik.runs.schemas as schemas
import mantik.utils.env_vars as env_vars


logger = logging.getLogger(__name__)


def get_gpu_info() -> list:
    import GPUtil

    gpus = GPUtil.getGPUs()

    gpu_info_list = []

    for gpu in gpus:
        gpu_info = {
            "Name": gpu.name,
            "ID": str(gpu.id),
            "Driver": gpu.driver,
            "TotalMemory": str(gpu.memoryTotal),
        }

        gpu_info_list.append(gpu_info)

    return gpu_info_list


def get_system_details() -> dict:
    import cpuinfo
    import psutil

    system_details = {
        "Platform": platform.platform(),
        "CpuModel": cpuinfo.get_cpu_info().get("brand_raw"),
        "CpuCoreCount": psutil.cpu_count(),
        "TotalMemoryGB": psutil.virtual_memory().total / (1024**3),
        "GPUInfo": get_gpu_info(),
    }
    return {"SystemDetails": system_details}


@runs.cli.command("local")
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
    "--project-id",
    type=uuid.UUID,
    required=True,
    help=f"""Project ID on Mantik.

        If not specified, it is inferred from the environment variable
        {env_vars._PROJECT_ID_ENV_VAR}.

    """,
    envvar=env_vars._PROJECT_ID_ENV_VAR,
)
@click.option(
    "--data-repository-id",
    type=uuid.UUID,
    default=None,
    help=f"""Data repository ID on Mantik

        If not specified, it is inferred from the environment variable
        {env_vars._DATA_REPOSITORY_ID_ENV_VAR}.

    """,
    envvar=env_vars._DATA_REPOSITORY_ID_ENV_VAR,
)
@click.option(
    "--experiment-repository-id",
    type=uuid.UUID,
    required=True,
    help=f"""Experiment repository ID on Mantik

        If not specified, it is inferred from the environment variable
        {env_vars._EXPERIMENT_REPOSITORY_ID_ENV_VAR}.

    """,
    envvar=env_vars._EXPERIMENT_REPOSITORY_ID_ENV_VAR,
)
@click.option(
    "--code-repository-id",
    type=uuid.UUID,
    required=True,
    help=f"""Code repository ID on Mantik

        If not specified, it is inferred from the environment variable
        {env_vars._CODE_REPOSITORY_ID_ENV_VAR}.

    """,
    envvar=env_vars._CODE_REPOSITORY_ID_ENV_VAR,
)
@click.option(
    "--branch",
    default=None,
    type=str,
    help="Name of the code repository's branch you want to use for this run",
    required=False,
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
    "--backend-config-system-info",
    type=bool,
    default=True,
    help="Populate the backend config JSON with system info.",
)
@click.option(
    "--parameter", "-P", show_default=True, default=lambda: [], multiple=True
)
@_main_options.VERBOSE
def run_project(
    run_name: str,
    mlproject_path: pathlib.Path,
    entry_point: str,
    parameter: t.List[str],
    verbose: bool,  # noqa
    project_id: uuid.UUID,
    data_repository_id: t.Optional[uuid.UUID],
    experiment_repository_id: uuid.UUID,
    code_repository_id: uuid.UUID,
    branch: t.Optional[str],
    commit: t.Optional[str],
    backend_config_system_info: bool,
) -> None:
    """Run an MLflow project locally and save the results in Mantik API

    Note that `MLPROJECT_PATH` is the relative path to the MLflow project file
    with your Code Repository as root.

    Remember that when you execute a run, the code is retrieved from your
    remote Git Code Repository. So make sure to commit and push your
    changes before executing a run!

    To find the respective required IDs make sure to check Mantik's UI

    """

    if branch is None and commit is None:
        raise ValueError("Either provide a branch or full commit hash to run")

    logger.debug("Parsing MLflow entry point parameters")
    parameters = cli_utils.dict_from_list(parameter)

    mantik_token = mantik.authentication.auth.get_valid_access_token()

    system_details = get_system_details() if backend_config_system_info else {}

    local_runs.run(
        data=schemas.RunConfiguration(
            name=run_name,
            experiment_repository_id=experiment_repository_id,
            code_repository_id=code_repository_id,
            branch=branch,
            commit=commit,
            data_repository_id=data_repository_id,
            mlflow_mlproject_file_path=mlproject_path.as_posix(),
            entry_point=entry_point,
            mlflow_parameters=parameters,
            backend_config=system_details,
        ),
        project_id=project_id,
        mantik_token=mantik_token,
    )
    click.echo("Done!")
