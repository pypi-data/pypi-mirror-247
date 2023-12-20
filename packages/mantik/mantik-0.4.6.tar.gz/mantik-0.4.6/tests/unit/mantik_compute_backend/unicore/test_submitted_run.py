import mlflow.entities as entities
import pytest

import mantik.testing.pyunicore as test_unicore
import mantik_compute_backend.unicore._properties as _properties


class TestSubmittedUnicoreRun:
    def test_run_id(self, example_job_properties):
        run = test_unicore._create_run(properties=example_job_properties)
        expected = "test-job"

        result = run.run_id

        assert result == expected

    @pytest.mark.parametrize(
        ("will_be_successful", "expected"),
        [
            (
                True,
                True,
            ),
            (
                False,
                False,
            ),
        ],
    )
    def test_wait(self, will_be_successful, expected, example_job_properties):
        run = test_unicore._create_run(
            will_be_successful=will_be_successful,
            properties=example_job_properties,
        )
        result = run.wait()

        assert result == expected

    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (
                _properties.Status.STAGING_IN,
                entities.RunStatus.SCHEDULED,
            ),
            (
                _properties.Status.READY,
                entities.RunStatus.SCHEDULED,
            ),
            (
                _properties.Status.QUEUED,
                entities.RunStatus.SCHEDULED,
            ),
            (
                _properties.Status.RUNNING,
                entities.RunStatus.RUNNING,
            ),
            (
                _properties.Status.STAGING_OUT,
                entities.RunStatus.RUNNING,
            ),
            (
                _properties.Status.SUCCESSFUL,
                entities.RunStatus.FINISHED,
            ),
            (
                _properties.Status.FAILED,
                entities.RunStatus.FAILED,
            ),
            (
                _properties.Status.UNKNOWN,
                entities.RunStatus.RUNNING,
            ),
        ],
    )
    def test_get_status(self, status, expected, example_job_properties):
        run = test_unicore._create_run(
            status=status, properties=example_job_properties
        )
        result = run.get_status()

        assert result == expected

    def test_cancel(self, example_job_properties):
        run = test_unicore._create_run(properties=example_job_properties)

        run.cancel()
