import json
import pathlib

import fastapi.testclient
import mlflow.projects
import pytest

import mantik.compute_backend as compute_backend
import mantik.testing as testing
import mantik.utils.unicore.zip as unicore_zip
import mantik_compute_backend
import mantik_compute_backend.settings as settings
import tokens.verifier as _verifier


@pytest.fixture(scope="function")
def client(monkeypatch) -> fastapi.testclient.TestClient:
    monkeypatch.setattr(
        _verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )
    app = mantik_compute_backend.app.create_app(global_path_prefix="")

    return fastapi.testclient.TestClient(app)


@pytest.fixture(scope="function")
def client_suppressing_raise(monkeypatch) -> fastapi.testclient.TestClient:
    monkeypatch.setattr(
        _verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )
    app = mantik_compute_backend.app.create_app(global_path_prefix="")

    return fastapi.testclient.TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="function")
def client_with_small_size_limitation(
    monkeypatch,
) -> fastapi.testclient.TestClient:
    monkeypatch.setattr(
        _verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )
    app = mantik_compute_backend.app.create_app(global_path_prefix="")

    def get_settings_override() -> settings.Settings:
        return settings.Settings(max_file_size=1)

    app.dependency_overrides[settings.get_settings] = get_settings_override

    return fastapi.testclient.TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def submit_run_request_data():
    return {
        "run_name": "test-run-name",
        "entry_point": "main",
        "mlflow_parameters": json.dumps({"foo": "bar"}),
        "unicore_user": "bar",
        "compute_budget_account": "baz",
        "unicore_password": "bam",
        "compute_backend_config": "compute-backend-config.json",
        "experiment_id": "1",
        "mlflow_tracking_uri": "foo",
        "mlflow_tracking_token": "aasdf",
    }


@pytest.fixture(scope="session")
def mlproject_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).parent / "../../../tests/resources/test-project"
    )


@pytest.fixture()
def example_project(
    mlproject_path,
) -> mlflow.projects._project_spec.Project:
    return mlflow.projects.utils.load_project(mlproject_path)


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
            )
        ),
        resources=compute_backend.config.resources.Resources(queue="batch"),
        exclude=[],
    )


@pytest.fixture()
def zipped_content(mlproject_path, example_config):
    return unicore_zip.zip_directory_with_exclusion(
        mlproject_path, example_config
    )


@pytest.fixture()
def submit_run_request_files(zipped_content):
    return {"mlproject_zip": zipped_content}


@pytest.fixture(scope="session")
def broken_mlproject_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "../../resources/broken-project"


@pytest.fixture(scope="function")
def broken_config() -> compute_backend.config.core.Config:
    return compute_backend.config.core.Config(
        api_url="test-url",
        user="user",
        password="password",
        project="test-project",
        environment=compute_backend.config.environment.Environment(
            execution=compute_backend.config.executable.Apptainer(
                path=pathlib.Path("/mantik-test.sif"), type="remote"
            )
        ),
        resources=compute_backend.config.resources.Resources(queue="batch"),
        exclude=[],
    )


@pytest.fixture()
def broken_zipped_content(broken_mlproject_path, broken_config):
    return unicore_zip.zip_directory_with_exclusion(
        broken_mlproject_path, broken_config
    )
