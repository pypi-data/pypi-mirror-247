import datetime
import json
import os
import pathlib

import pytest

import mantik.compute_backend as compute_backend
import mantik.compute_backend.config.core as core
import mantik.unicore as unicore
import mantik.unicore.credentials as unicore_credentials
import mantik.utils as utils

FILE_DIR = pathlib.Path(__file__).parent


@pytest.fixture
def required_config_env_vars():
    return {
        unicore_credentials._USERNAME_ENV_VAR: "test-user",
        unicore_credentials._PASSWORD_ENV_VAR: "test-password",
        core._PROJECT_ENV_VAR: "test-project",
    }


@pytest.fixture(scope="session")
def mlproject_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../../tests/resources/test-project"
    )


@pytest.fixture(scope="session")
def invalid_config_type() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent
        / "../../../../../tests/resources/broken-project/compute-backend-config.md"  # noqa: E501
    )


@pytest.fixture(scope="session")
def config_with_errors() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent / "../../../../../tests/resources/"
        "test-project/config-with-errors.yaml"
    )


@pytest.fixture(scope="session")
def compute_backend_config_yaml(mlproject_path) -> pathlib.Path:
    """Return the UNICORE config in YAML format.

    Doesn't contain. `Environment` section

    """
    return pathlib.Path(f"{str(mlproject_path)}/compute-backend-config.yaml")


@pytest.fixture(scope="session")
def compute_backend_config_json(mlproject_path) -> pathlib.Path:
    return pathlib.Path(f"{str(mlproject_path)}/compute-backend-config.json")


@pytest.fixture()
def unset_tracking_token_env_var_before_execution():
    if utils.mlflow.TRACKING_TOKEN_ENV_VAR in os.environ:
        del os.environ[utils.mlflow.TRACKING_TOKEN_ENV_VAR]


@pytest.fixture(scope="function")
def example_config() -> compute_backend.config.core.Config:
    return compute_backend.config.core.Config(
        api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=compute_backend.config.environment.Environment(
            execution=compute_backend.config.executable.Apptainer(
                path=pathlib.Path("mantik-test.sif"),
            ),
            variables={"SRUN_CPUS_PER_TASK": 100},
        ),
        resources=compute_backend.config.resources.Resources(queue="batch"),
        exclude=["*.py", "*.sif"],
    )


@pytest.fixture()
def example_job_property_response() -> dict:
    with open(
        FILE_DIR
        / "../../../resources/unicore-responses/job-property-response.json",
    ) as f:
        return json.load(f)


@pytest.fixture()
def example_job_properties():
    return unicore.properties.Properties(
        status=unicore.properties.Status.SUCCESSFUL,
        logs=[],
        owner="owner",
        site_name="siteName",
        consumed_time=unicore.properties.ConsumedTime(
            total=datetime.timedelta(seconds=1),
            queued=datetime.timedelta(seconds=2),
            stage_in=datetime.timedelta(seconds=3),
            pre_command=datetime.timedelta(seconds=4),
            main=datetime.timedelta(seconds=5),
            post_command=datetime.timedelta(seconds=6),
            stage_out=datetime.timedelta(seconds=7),
        ),
        current_time=datetime.datetime(
            2000, 1, 1, tzinfo=unicore.properties.TZ_OFFSET
        ),
        submission_time=datetime.datetime(
            2000, 1, 1, tzinfo=unicore.properties.TZ_OFFSET
        ),
        termination_time=datetime.datetime(
            2000, 1, 2, tzinfo=unicore.properties.TZ_OFFSET
        ),
        status_message="statusMessage",
        tags=["tag"],
        resource_status="resourceStatus",
        name="name",
        exit_code="0",
        queue="queue",
        submission_preferences={"any": "preferences"},
        resource_status_message="resourceStatusMessage",
        acl=["acl"],
        batch_system_id="batchSystemID",
    )


@pytest.fixture()
def example_config_for_python() -> compute_backend.config.core.Config:
    return compute_backend.config.core.Config(
        api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=compute_backend.config.environment.Environment(
            execution=compute_backend.config.executable.Python(
                path=pathlib.Path("/venv"),
            )
        ),
        resources=compute_backend.config.resources.Resources(queue="batch"),
        exclude=["*.sif"],
    )
