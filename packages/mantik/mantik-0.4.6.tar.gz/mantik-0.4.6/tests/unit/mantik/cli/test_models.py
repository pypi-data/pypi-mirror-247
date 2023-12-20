import os
import unittest.mock
import uuid

import click.testing
import pytest

import mantik.cli.main as main
import mantik.cli.models.models

GROUP_NAME = mantik.cli.models.models.GROUP_NAME


SAMPLE_UUID = uuid.uuid4()


@pytest.fixture
def sample_uuid_str() -> str:
    return str(SAMPLE_UUID)


@pytest.fixture
def mock_authentication():
    with unittest.mock.patch(
        "mantik.authentication.auth.get_valid_access_token",
        return_value="1234-token",
    ):
        yield


@pytest.fixture
def mock_project_id_env_var(sample_uuid_str):
    os.environ[mantik.cli.models.models._PROJECT_ID_ENV_VAR] = sample_uuid_str
    yield
    os.unsetenv(mantik.cli.models.models._PROJECT_ID_ENV_VAR)


@pytest.fixture
def cli_test_runner():
    yield click.testing.CliRunner()


def test_get_all_project_models(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.get_all"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [GROUP_NAME, "list", "--project-id", sample_uuid_str],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_get_model(mock_authentication, cli_test_runner, sample_uuid_str):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.get_one"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "get-one",
                "--model-id",
                sample_uuid_str,
                "--project-id",
                sample_uuid_str,
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_delete_model(
    mock_authentication,
    mock_project_id_env_var,
    cli_test_runner,
    sample_uuid_str,
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.delete"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [GROUP_NAME, "delete", "--model-id", sample_uuid_str],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_create_model_entry(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.add"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "add",
                "--project-id",
                sample_uuid_str,
                "--uri",
                "URI",
                "--location",
                "something://somewhere.com",
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


def test_update_model_entry(
    mock_authentication, cli_test_runner, sample_uuid_str
):
    with unittest.mock.patch(
        "mantik.utils.mantik_api.models.update"
    ) as mocked_function:
        result = cli_test_runner.invoke(
            main.cli,
            [
                GROUP_NAME,
                "update",
                "--project-id",
                sample_uuid_str,
                "--model-id",
                sample_uuid_str,
                "--uri",
                "URI",
                "--location",
                "something://somewhere.com",
            ],
        )
        assert result.exit_code == 0
        mocked_function.assert_called()


@pytest.mark.parametrize(
    "mlflow_params,expected",
    [
        ('{"hello":"world"}', {"hello": "world"}),
        (None, None),
    ],
)
def test_mlflow_parameters_decoder(mlflow_params, expected):
    assert (
        mantik.cli.models.models.mlflow_parameters_decoder(
            None, None, mlflow_params
        )
        == expected
    )


def test_mlflow_parameters_decoder_raises_error_on_wrong_format():
    with pytest.raises(TypeError):
        mantik.cli.models.models.mlflow_parameters_decoder(
            None, None, "i am a broken json string"
        )
