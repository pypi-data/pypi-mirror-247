"""Interact with trained models in mantik api"""
import dataclasses
import typing as t
import uuid

from mantik.utils.mantik_api.client import logger
from mantik.utils.mantik_api.client import send_request_to_mantik_api

T = t.TypeVar("T")


def optional_cast(_type: T, optional_value: t.Optional[t.Any]) -> t.Optional[T]:
    if optional_value is None:
        return None

    return _type(optional_value)


@dataclasses.dataclass
class ModelBase:
    uri: str
    location: str
    connection_id: t.Optional[uuid.UUID]
    mlflow_parameters: t.Optional[dict]


@dataclasses.dataclass
class GetModel(ModelBase):
    model_id: uuid.UUID
    model_repository: dict

    @classmethod
    def from_json(cls, json_str):
        return cls(
            model_id=uuid.UUID(json_str["modelId"]),
            uri=json_str["uri"],
            location=json_str["location"],
            connection_id=optional_cast(uuid.UUID, json_str["connectionId"]),
            mlflow_parameters=json_str["mlflowParameters"],
            model_repository=json_str["modelRepository"],
        )


@dataclasses.dataclass
class PostPutModel(ModelBase):
    model_repository_id: t.Optional[uuid.UUID]

    def to_dict(self):
        return {
            "uri": self.uri,
            "location": self.location,
            "connectionId": optional_cast(str, self.connection_id),
            "mlflowParameters": self.mlflow_parameters,
            "modelRepositoryId": optional_cast(str, self.model_repository_id),
        }


def get_all(
    project_id: uuid.UUID,
    token: str,
) -> t.List[GetModel]:
    """Retrieves trained model entries through the Mantik API"""

    endpoint = f"/mantik-api/projects/{str(project_id)}/models/trained"
    response = send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return [GetModel.from_json(model) for model in response.json()["models"]]


def get_one(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
) -> GetModel:
    """Retrieves a trained model entry from the Mantik API"""

    endpoint = (
        f"/mantik-api/projects/{str(project_id)}/models/trained/{str(model_id)}"
    )
    response = send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return GetModel.from_json(response.json())


def delete(
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
):
    """Deletes a trained model entry through the Mantik API"""

    endpoint = (
        f"/mantik-api/projects/{str(project_id)}/models/trained/{str(model_id)}"
    )
    send_request_to_mantik_api(
        method="DELETE", data={}, url_endpoint=endpoint, token=token
    )
    logger.info(f"Model with ID: {model_id} has been deleted")


def add(
    new_model_schema: PostPutModel,
    project_id: uuid.UUID,
    token: str,
) -> uuid.UUID:
    """Creates a trained model entry through the Mantik API"""

    data = new_model_schema.to_dict()
    endpoint = f"/mantik-api/projects/{str(project_id)}/models/trained"
    response = send_request_to_mantik_api(
        method="POST", data=data, url_endpoint=endpoint, token=token
    )
    new_model_id = response.json()["modelId"]
    logger.info(f"A model with ID: {new_model_id} has been created")

    return uuid.UUID(new_model_id)


def update(
    updated_model_schema: PostPutModel,
    project_id: uuid.UUID,
    model_id: uuid.UUID,
    token: str,
):
    """Updates a trained model entry through the Mantik API"""

    data = updated_model_schema.to_dict()
    endpoint = (
        f"/mantik-api/projects/{str(project_id)}/models/trained/{str(model_id)}"
    )
    send_request_to_mantik_api(
        method="PUT", data=data, url_endpoint=endpoint, token=token
    )
    logger.info(f"Model with ID: {str(model_id)} has been updated")
