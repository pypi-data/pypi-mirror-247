import json
from typing import Any, Callable, ClassVar, Dict, Generic, Optional, Type, TypeVar
from scale_egp.sdk.client import EGPClient
from scale_egp.sdk.collections.models_api.model_templates import ModelTemplateCollection
from scale_egp.sdk.collections.models_api.models import ModelCollection
from scale_egp.sdk.models.model_api_models import (
    ModelAlias,
    ModelAliasRequest,
    ModelTemplate,
    ModelTemplateRequest,
)
from scale_egp.sdk.models.model_schemas.model_schemas import MODEL_SCHEMAS
from scale_egp.utils.api_utils import APIEngine
from scale_egp.utils.model_utils import BaseModel
from argh import arg


EntityT = TypeVar("EntityT", bound=BaseModel)
RequestT = TypeVar("RequestT", bound=BaseModel)


def read_json_file(filename: str) -> Any:
    with open(filename, "r", encoding="utf-8") as f:
        return json.loads(f.read())


CollectionGetter = Callable[[EGPClient], APIEngine]


class EGPClientFactory:
    def __init__(
        self,
    ):
        self.client: Optional[EGPClient] = None

    def set_client(self, **kwargs):
        self.client = EGPClient(**kwargs)

    def get_client(self) -> EGPClient:
        if self.client is None:
            self.client = EGPClient()
        return self.client


class CollectionCRUDCommands(Generic[EntityT, RequestT]):
    def __init__(
        self,
        client_factory: EGPClientFactory,
        entity_type: Type[EntityT],
        request_type: Type[RequestT],
        collection_type: Type[APIEngine],
    ):
        self._client_factory = client_factory
        self._entity_type = entity_type
        self._request_type = request_type
        self._collection_type = collection_type

    def _get_collection_instance(self) -> APIEngine:
        return self._collection_type(self._client_factory.get_client())

    def _transform_entity_json(self, entity_dict: Dict[str, Any]) -> Dict[str, Any]:
        return entity_dict

    def _create(self, request_dict: Any) -> EntityT:
        assert isinstance(request_dict, dict)
        # add client account id if not set in file
        request_dict["account_id"] = request_dict.get(
            "account_id", self._client_factory.get_client().account_id
        )
        request_obj = self._request_type(**request_dict)
        collection = self._get_collection_instance()
        response = collection._post(getattr(collection, "_sub_path"), request_obj)
        assert response.status_code == 200
        response_dict = response.json()
        assert isinstance(response_dict, dict)
        return self._entity_type(**response_dict)

    @arg("filename", help="file to load")
    def create(self, filename: str) -> EntityT:
        request_dict = read_json_file(filename)
        return self._create(request_dict)

    def get(self, id: str) -> EntityT:
        collection = self._get_collection_instance()
        sub_path = f"{collection._sub_path}/{id}"
        response = collection._get(sub_path)
        assert response.status_code == 200
        response_dict = response.json()
        assert isinstance(response_dict, dict)
        return self._entity_type(**response_dict)


class ModelAliasCRUDCommands(CollectionCRUDCommands[ModelAlias, ModelAliasRequest]):
    def __init__(
        self,
        client_factory: EGPClientFactory,
    ):
        super().__init__(client_factory, ModelAlias, ModelAliasRequest, ModelCollection)

    @arg("filename", help="file to load")
    def create(self, model_template_id: str, filename: str) -> EntityT:
        request_dict = read_json_file(filename)
        request_dict["model_template_id"] = model_template_id
        return self._create(request_dict)

    @arg("filename", help="Model request")
    def execute(self, model_id: str, filename: str) -> EntityT:
        model_alias = self.get(model_id)
        model_template = ModelTemplateCRUDCommands(self._client_factory).get(
            model_alias.model_template_id
        )
        model_type = model_template.model_type
        model_request_cls, model_response_cls = MODEL_SCHEMAS[model_type]
        request_dict = read_json_file(filename)
        assert isinstance(request_dict, dict)
        request_obj = model_request_cls(**request_dict)
        collection = self._get_collection_instance()
        sub_path = f"{collection._sub_path}/{model_id}/execute"
        response = collection._post(
            sub_path=sub_path,
            request=request_obj,
            timeout=10 * 60,  # 10 minutes
        )
        assert response.status_code == 200
        return model_response_cls(**response.json())


class ModelTemplateCRUDCommands(CollectionCRUDCommands[ModelTemplate, ModelTemplateRequest]):
    def __init__(
        self,
        client_factory: EGPClientFactory,
    ):
        super().__init__(
            client_factory, ModelTemplate, ModelTemplateRequest, ModelTemplateCollection
        )

    def _transform_entity_json(self, entity_dict: Dict[str, Any]) -> Dict[str, Any]:
        if entity_dict.get("vendor_configuration") is not None:
            entity_dict["model_vendor"] = "LLMENGINE"
        return entity_dict
