import uuid

import pytest
import requests

import mantik.utils.mantik_api.models as models


@pytest.fixture(scope="session")
def model_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture(scope="session")
def project_id() -> uuid.UUID:
    return uuid.uuid4()


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_model(
    mock_mantik_api_request,
    info_caplog,
    status_code,
    expected,
    model_id,
    project_id,
):
    sample_model_schema = {
        "modelId": str(model_id),
        "uri": "string",
        "location": "string",
        "connectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "mlflowParameters": "{}",
        "modelRepository": "{}",
    }

    with mock_mantik_api_request(
        method="GET",
        end_point=f"/mantik-api/projects/{str(project_id)}/"
        f"models/trained/{str(model_id)}",
        status_code=status_code,
        json_response=sample_model_schema,
        expected_error=expected,
    ) as (m, error):
        retrieved_model = models.get_one(
            project_id=project_id, model_id=model_id, token="test_token"
        )
        assert retrieved_model == models.GetModel.from_json(sample_model_schema)
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_get_all_project_models(
    mock_mantik_api_request,
    info_caplog,
    status_code,
    expected,
    model_id,
    project_id,
):
    sample_model_schema = {
        "modelId": str(model_id),
        "uri": "string",
        "location": "string",
        "connectionId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "mlflowParameters": "{}",
        "modelRepository": "{}",
    }

    with mock_mantik_api_request(
        method="GET",
        end_point=f"/mantik-api/projects/{str(project_id)}/models/trained",
        status_code=status_code,
        json_response={
            "totalRecords": 1,
            "models": [sample_model_schema],
        },
        expected_error=expected,
    ) as (m, error):
        retrieved_model = models.get_all(
            project_id=project_id, token="test_token"
        )
        assert retrieved_model == [
            models.GetModel.from_json(sample_model_schema)
        ]
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


@pytest.mark.parametrize(
    ("status_code", "expected"), [(204, None), (404, requests.HTTPError())]
)
def test_delete_model_entry(
    mock_mantik_api_request,
    info_caplog,
    status_code,
    expected,
    model_id,
    project_id,
):
    with mock_mantik_api_request(
        method="DELETE",
        end_point=f"/mantik-api/projects/{str(project_id)}/"
        f"models/trained/{str(model_id)}",
        status_code=status_code,
        json_response={},
        expected_error=expected,
    ) as (m, error):
        models.delete(
            project_id=project_id,
            model_id=model_id,
            token="test_token",
        )
        assert any(
            f"Model with ID: {model_id} has been deleted" in message
            for message in info_caplog.messages
        )
    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )


def test_create_model_entry(
    mock_mantik_api_request,
    add_data_repository,
    info_caplog,
    project_id,
    model_id,
):
    new_model_schema = models.PostPutModel(
        uri="s3://bucket/item.type",
        location="S3",
        connection_id=uuid.uuid4(),
        mlflow_parameters={},
        model_repository_id=None,
    )

    with mock_mantik_api_request(
        method="POST",
        end_point=f"/mantik-api/projects/{str(project_id)}/models/trained",
        status_code=201,
        json_response={"modelId": str(model_id)},
        expected_error=None,
    ):
        new_model_id = models.add(
            new_model_schema=new_model_schema,
            project_id=project_id,
            token="test_token",
        )
        assert new_model_id == model_id

        assert any(
            f"A model with ID: {model_id} has been created" in message
            for message in info_caplog.messages
        )


@pytest.mark.parametrize(
    ("status_code", "expected"), [(200, None), (404, requests.HTTPError())]
)
def test_update_model(
    mock_mantik_api_request,
    info_caplog,
    status_code,
    expected,
    model_id,
    project_id,
):
    updated_model_schema = models.PostPutModel(
        uri="s3://bucket/item.type",
        location="S3",
        connection_id=uuid.uuid4(),
        mlflow_parameters={},
        model_repository_id=None,
    )

    with mock_mantik_api_request(
        method="PUT",
        end_point=f"/mantik-api/projects/{str(project_id)}/"
        f"models/trained/{str(model_id)}",
        status_code=status_code,
        json_response={},
        expected_error=expected,
    ) as (m, error):
        models.update(
            project_id=project_id,
            model_id=model_id,
            updated_model_schema=updated_model_schema,
            token="test_token",
        )
        assert f"Model with ID: {str(model_id)} has been updated"

    if error:
        assert any(
            "Call to Mantik API" in message for message in info_caplog.messages
        )
