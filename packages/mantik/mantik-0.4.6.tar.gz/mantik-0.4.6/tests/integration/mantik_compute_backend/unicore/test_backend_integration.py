"""Integration tests for UNICORE.

**WARNING:** The UNICORE container takes up to 15-30 seconds to process a job,
hence be careful with the number of test cases used.


"""
import pathlib

import mlflow.projects as projects
import pytest

import mantik.compute_backend.config.core as core
import mantik.unicore.credentials as _unicore_credentials
import mantik.utils as utils
import mantik_compute_backend.unicore._properties as _properties
import mantik_compute_backend.unicore.backend as backend
import mantik_compute_backend.utils as mantik_compute_backend_utils

FILE_PATH = pathlib.Path(__file__).parent


@pytest.fixture()
def required_unicore_env_vars(unicore_credentials) -> dict:
    return {
        _unicore_credentials._USERNAME_ENV_VAR: unicore_credentials["user"],
        _unicore_credentials._PASSWORD_ENV_VAR: unicore_credentials["password"],
        core._PROJECT_ENV_VAR: "test-project",
        mantik_compute_backend_utils.mlflow.RUN_NAME_ENV_VAR: "my run name",
    }


RESOURCES = {
    "Queue": "batch",
    "Runtime": "1h",
    "Nodes": 1,
    "TotalCPUs": 1,
    "CPUsPerNode": 1,
    "MemoryPerNode": "1M",
}

EXPECTED_RESOURCE_MESSAGES = (
    "Queue=batch",
    "Runtime=3600",
    "Nodes=1",
    "TotalCPUs=1",
    "CPUsPerNode=1",
    "MemoryPerNode=1048576",
    "Project=test-project",
)


class TestUnicoreBackend:
    @pytest.mark.parametrize(
        (
            "entry_point",
            "params",
            "backend_config",
            "expected_job_status",
            "expected_log_messages",
        ),
        [
            # Test case: Apptainer with 1 env var
            #
            # * Test case will fail since no Apptainer image present in UNICORE
            #   container, thus the post command on login node won't be executed
            (
                "main",
                {"print": "test"},
                {
                    "Environment": {
                        "Variables": {"TEST_VAR": "test_value"},
                        "Apptainer": {
                            "Path": "/does/not/exist.sif",
                            "Type": "remote",
                        },
                        "PreRunCommandOnLoginNode": "echo precommand login node\n echo again",  # noqa E501
                        "PostRunCommandOnLoginNode": "echo postcommand login node",  # noqa E501
                        "PreRunCommandOnComputeNode": "echo precommand compute node",  # noqa E501
                        "PostRunCommandOnComputeNode": "echo postcommand compute node",  # noqa E501
                    },
                    "Resources": RESOURCES,
                },
                _properties.Status.FAILED,
                [
                    *EXPECTED_RESOURCE_MESSAGES,
                    "MLFLOW_RUN_ID=",
                    "; export MLFLOW_RUN_ID",
                    'TEST_VAR="test_value"; export TEST_VAR',
                    "echo precommand login node\n echo again",
                    (
                        "echo precommand compute node && "
                        "srun apptainer run "
                        "/does/not/exist.sif "
                        "python main.py test && "
                        "echo postcommand compute node"
                    ),
                ],
            ),
            # Test case: Python with 1 env var
            #
            # * Test case will fail since no venv present in UNICORE container,
            #   thus the post command on login node won't be executed
            (
                "main",
                {"print": "test"},
                {
                    "Environment": {
                        "Variables": {"TEST_VAR": "test_value"},
                        "Python": {
                            "Path": "/does/not/exist",
                        },
                        "PreRunCommandOnLoginNode": "echo precommand login node\n echo again",  # noqa E501
                        "PostRunCommandOnLoginNode": "echo postcommand login node",  # noqa E501
                        "PreRunCommandOnComputeNode": "echo precommand compute node",  # noqa E501
                        "PostRunCommandOnComputeNode": "echo postcommand compute node",  # noqa E501
                    },
                    "Resources": RESOURCES,
                },
                _properties.Status.FAILED,
                [
                    *EXPECTED_RESOURCE_MESSAGES,
                    "MLFLOW_RUN_ID=",
                    "; export MLFLOW_RUN_ID",
                    'TEST_VAR="test_value"; export TEST_VAR',
                    "echo precommand login node\n echo again",
                    (
                        "echo precommand compute node && "
                        "source /does/not/exist/bin/activate && "
                        "python main.py test && "
                        "echo postcommand compute node"
                    ),
                ],
            ),
            # Test case: No execution environment and echo entry point
            #
            # * Should succeed
            # * Pre/postcommand will be executed on login node, hence no modules
            #   loaded here. Modules would make the pre command fail (no modules
            #   in UNICORE container), and the main application will not be
            #   executed, as well as the post command.
            (
                "echo",
                {"output": "test"},
                {
                    "Environment": {
                        "Variables": {"TEST_VAR": "test_value"},
                        "PreRunCommandOnLoginNode": "echo precommand login node\n echo again",  # noqa E501
                        "PostRunCommandOnLoginNode": "echo postcommand login node",  # noqa E501
                    },
                    "Resources": RESOURCES,
                },
                _properties.Status.SUCCESSFUL,
                [
                    "Launched pre command <echo precommand login node\n "
                    "echo again>\n",
                    "Executing command: echo precommand login node\n "
                    "echo again",
                    "Execution on login node",
                    *EXPECTED_RESOURCE_MESSAGES,
                    'TEST_VAR="test_value"; export TEST_VAR',
                    "MLFLOW_RUN_ID=",
                    "; export MLFLOW_RUN_ID",
                    "echo test",
                ],
            ),
        ],
    )
    def test_run(
        self,
        tmp_path,
        env_vars_set,
        unicore_api_url,
        required_unicore_env_vars,
        example_project_path,
        entry_point,
        params,
        backend_config,
        expected_job_status,
        expected_log_messages,
    ):
        backend_config = {
            **backend_config,
            "UnicoreApiUrl": unicore_api_url,
            # Following values are set by MLflow before running a project.
            projects.PROJECT_STORAGE_DIR: example_project_path.as_posix(),
        }

        expected_log_messages.extend(
            [
                # MLflow Tracking URI should be set by compute backend
                f'MLFLOW_TRACKING_URI="file://{tmp_path.as_posix()}/mlruns"; export MLFLOW_TRACKING_URI',  # noqa: E501
            ]
        )

        # Following env vars must be set for the config.
        tracking_uri = tmp_path / "mlruns"
        with env_vars_set(
            {
                **required_unicore_env_vars,
                # Point MLFLOW_TRACKING_URI to a temporary directory
                utils.mlflow.TRACKING_URI_ENV_VAR: tracking_uri.as_uri(),  # noqa: E501
            }
        ):
            result = backend.UnicoreBackend().run(
                project_uri=example_project_path.as_posix(),
                entry_point=entry_point,
                params=params,
                version=None,
                backend_config=backend_config,
                tracking_uri=None,
                experiment_id=None,
            )
            # Wait for job to fail or succeed
            result.wait()
            result_log_messages = "\n".join(result._job.properties.logs)

        for exp in expected_log_messages:
            assert exp in result_log_messages, f"Message {exp!r} not in logs"
        assert result._status == expected_job_status
