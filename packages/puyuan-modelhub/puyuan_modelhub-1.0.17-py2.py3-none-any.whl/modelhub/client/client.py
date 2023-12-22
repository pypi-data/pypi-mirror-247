import requests
from pydantic import BaseModel, root_validator, validator
import os
from modelhub.common.types import (
    TextGenerationOutput,
    BaseMessage,
    convert_dicts_to_messages,
    convert_messages_to_dicts,
)
import httpx
from typing import Optional, Dict, List, Any, Literal
import json
import retrying


class APIConnectionError(Exception):
    """APIConnectionError: Error when connecting to the API"""

    def __init__(self, message: str):
        super().__init__(message)


class AuthenticationError(Exception):
    """AuthenticationError: Error when authentication fails"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class APIRateLimitError(Exception):
    """RateLimitError: Error when the API rate limit is exceeded"""

    def __init__(self, message: str):
        super().__init__(message)


class ModelhubClient(BaseModel):
    """
    ModelhubClient: A Python client for the Modelhub API
    """

    user_name: str = os.getenv("MODELHUB_USER_NAME", "")
    """user name for authentication"""
    user_password: str = os.getenv("MODELHUB_USER_PASSWORD", "")
    """user password for authentication"""
    host: str = os.getenv("MODELHUB_HOST", "")
    model: str = ""
    max_retries: int = 3
    wait_fixed: int = 1000
    timeout: httpx.Timeout = httpx.Timeout(10.0, connect=10.0)
    """host URL of the Modelhub API"""
    """list of supported models"""
    headers: Dict[str, Any] = {}

    _supported_models = None

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"

    @root_validator
    def set_auth(cls, values):
        values["host"] = values["host"].rstrip("/")
        values["headers"][
            "Authorization"
        ] = f"{values['user_name']}:{values['user_password']}"
        return values

    @property
    def supported_models(self) -> List[Dict[str, Any]]:
        """Get a list of supported models from the Modelhub API"""
        if self._supported_models is None:
            object.__setattr__(self, "_supported_models", self._get_supported_models())
        return self._supported_models

    @retrying.retry(
        wait_fixed=wait_fixed,
        stop_max_attempt_number=max_retries,
        retry_on_exception=lambda e: not isinstance(e, AuthenticationError),
    )
    def _get(
        self,
        url: str,
        params: Dict[str, Any] = None,
        method: Literal["get", "post"] = "get",
        **kwargs,
    ) -> Any:
        """Make a GET request"""
        req_func = getattr(requests, method)
        response = req_func(url, params=params, headers=self.headers, **kwargs)
        if response.status_code == 401:
            raise AuthenticationError()
        if response.status_code == 500:
            raise ValueError(response.json())
        if response.status_code == 501:
            raise APIConnectionError(response.json())
        if response.status_code == 502:
            raise APIRateLimitError(response.json())
        return response

    def _get_supported_models(self) -> List[str]:
        """Get a list of supported models from the Modelhub API"""
        response = self._get(
            self.host + "/models",
        )
        return response.json()["models"]

    def get_supported_params(self, model: str) -> List[str]:
        """
        Get a list of supported parameters for a given model from the Modelhub API
        params:
            model: the model name
        """
        response = self._get(
            self.host + "/models/" + model,
        )
        return response.json()["params"]

    def n_tokens(self, prompt: str, model: str = "", params={}) -> int:
        """
        Get the number of tokens in a prompt
        params:
            prompt: the prompt
            model: the model name
        """
        model = model or self.model
        if model not in self.supported_models:
            raise ValueError(f"Model {model} not supported")
        response = self._get(
            self.host + "/tokens",
            json={
                "prompt": prompt,
                "model": model or self.model,
                "params": params,
            },
            method="post",
        )
        return response.json()

    def chat(
        self,
        prompt: str,
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
    ):
        """
        Chat with a model
        params:
            prompt: the prompt to start the chat
            model: the model name
            parameters: the parameters for the model
        """
        model = model or self.model
        if model not in self.supported_models:
            raise ValueError(f"Model {model} not supported")
        parameters["history"] = convert_messages_to_dicts(history)
        response = self._get(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model or self.model,
                "parameters": parameters,
            },
            method="post",
        )
        try:
            response = response.json()
        except:
            return response.text
        if "history" in response:
            response["history"] = convert_dicts_to_messages(response["history"])
        return response

    def stream_chat(
        self,
        prompt: str,
        model: str,
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
    ) -> Any:
        """
        Stream chat with a model
        params:
            prompt: the prompt to start the chat
            model: the model name
            parameters: the parameters for the model
        """
        parameters["history"] = convert_messages_to_dicts(history)
        response = self._get(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
                "stream": True,
            },
            method="post",
            stream=True,
        )
        for token in response.iter_lines(delimiter=b"\r\n\r\n"):
            if token:
                try:
                    yield json.loads(token)
                except Exception as e:
                    yield json.loads(token[5:])

    def get_embeddings(
        self, prompt: str, model: str, parameters: Dict[str, Any] = {}
    ) -> Any:
        """
        Get embeddings from a model
        params:
            prompt: the prompt to start the chat
            model: the model name
            parameters: the parameters for the model
        """
        response = self._get(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
            method="post",
        )
        return response.json()


class VLMClient(ModelhubClient):
    """Visual Language Model Client"""

    def chat(self, prompt, image_path, model="cogvlm", parameters={}, **kwargs):
        """
        Chat with a model
        params:
            prompt: the prompt to start the chat
            image_path: the path to the image
            model: the model name
            parameters: the parameters for the model
        """
        image_path = self._get(
            self.host + "/upload",
            files={"file": open(image_path, "rb")},
            params={
                "user_name": self.user_name,
                "user_password": self.user_password,
            },
            method="post",
        ).json()["file_path"]
        parameters["image_path"] = image_path
        return super().chat(prompt=prompt, model=model, parameters=parameters, **kwargs)
