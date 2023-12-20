import uuid

import pytest

import mantik.runs.schemas as run_schemas
import mantik.utils.mantik_api.code_repository as code_api
import mantik.utils.mantik_api.experiment_repository as experiment_api


@pytest.fixture(scope="session")
def sample_experiment_repository_id():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_code_repository_id():
    return uuid.uuid4()


@pytest.fixture(scope="session")
def sample_project_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture()
def sample_experiment_repository(sample_experiment_repository_id):
    return experiment_api.ExperimentRepository(
        experiment_repository_id=sample_experiment_repository_id,
        mlflow_experiment_id="123",
        name="Name",
        artifact_location="somewhere.com",
    )


@pytest.fixture()
def sample_code_repository(sample_code_repository_id):
    return code_api.CodeRepository(
        code_repository_id=sample_code_repository_id,
        code_repository_name="Name",
        uri="some/uri.git",
        access_token="1234",
    )


@pytest.fixture(scope="session")
def sample_run_configuration(
    sample_experiment_repository_id, sample_code_repository_id
) -> run_schemas.RunConfiguration:
    return run_schemas.RunConfiguration(
        name="Sample",
        experiment_repository_id=sample_experiment_repository_id,
        code_repository_id=sample_code_repository_id,
        branch="branch",
        commit="commit",
        data_repository_id=uuid.uuid4(),
        mlflow_mlproject_file_path="some/path/MLProject",
        entry_point="main",
        mlflow_parameters={"output": "hello world"},
        backend_config={},
    )


@pytest.fixture()
def fake_token():
    return "1234"
