import modelhub.server.models.api as api_module
from ..models.api import ModelhubModel
import modelhub.server.models.local as local_module
from modelhub.server.models.errors import *
from typing import List, Dict
from pydantic import BaseModel, Field
from ..lib.config import ModelConfig, get_config, LocalModelConfig
import time
from ..lib.local_models import check_server_running, start_server
from loguru import logger
import os


class ModelCard(BaseModel):
    id: str
    object: str = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "owner"


class ModelList(BaseModel):
    object: str = "list"
    data: List[ModelCard] = []


def validate_models(module, configs: List[ModelConfig]) -> Dict[str, ModelConfig]:
    for config in configs:
        if not hasattr(module, config.model_class):
            raise ModelNotFoundError(f"model {config.model_class} not found in models")
    return {config.name: config for config in configs}


class ModelFactory(object):
    def __init__(
        self, api_models: List[ModelConfig], local_models: List[LocalModelConfig] = []
    ) -> None:
        """提供各种模型，包括embedding的模型和llm的模型"""
        self._api_models: Dict[str, ModelConfig] = validate_models(
            api_module, api_models
        )
        self._local_models: Dict[str, LocalModelConfig] = validate_models(
            local_module, local_models
        )
        self._all_models = {**self._api_models, **self._local_models}
        self._cache = {}
        self._model_list = ModelList(
            data=[ModelCard(id=name) for name in self._all_models]
        )

    @property
    def models(self):
        return {
            name: {
                "is_llm": "chat" in config.model_types,
                "is_embedding": "embedding" in config.model_types,
                "is_audio": "audio" in config.model_types,
            }
            for name, config in self._all_models.items()
        }

    def list_models(self):
        return self._model_list

    def get_supported_params(self, model_name: str):
        return {"chat": [], "embedding": []}

    def get(self, id: str, kwargs: dict = {}):
        if id in self._cache:
            return self._cache[id]
        if not id in self._all_models:
            raise ModelNotFoundError(f"model {id} not found")
        kwargs = kwargs or self._all_models[id].model_kwargs
        if id in self._api_models:
            self._cache[id] = getattr(api_module, self._api_models[id].model_class)(
                **kwargs
            )
        elif get_config().app.is_sub_process:
            logger.info(f"loading local model {id}")
            self._cache[id] = getattr(local_module, self._local_models[id].model_class)(
                **kwargs
            )
        else:
            logger.info(f"checking server for {id}, PID: {os.getpid()}")
            running = check_server_running(self._local_models[id])
            if not running:
                logger.info(f"starting server for {id}")
                try:
                    start_server(self._local_models[id])
                except Exception as e:
                    raise ValueError(f"start server failed: {e}")
            self._cache[id] = ModelhubModel(
                host=f"http://127.0.0.1:{self._local_models[id].port}",
                model_name=self._local_models[id].name,
                user_name="subprocess",
            )

        return self._cache[id]


_model_factory = None


def get_model_factory():
    global _model_factory
    if _model_factory is None:
        _model_factory = ModelFactory(
            get_config().api_models, get_config().local_models
        )
    return _model_factory
