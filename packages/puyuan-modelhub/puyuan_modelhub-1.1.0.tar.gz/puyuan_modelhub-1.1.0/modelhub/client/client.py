import requests
from pydantic import BaseModel, root_validator, PrivateAttr
import os
from modelhub.common.types import (
    TextGenerationOutput,
    BaseMessage,
    ModelInfo,
    ModelInfoOutput,
    NTokensOutput,
    Transcription,
    TextGenerationStreamOutput,
    EmbeddingOutput,
    convert_messages_to_dicts,
    ChatParameters,
    CrossEncoderParams,
    CrossEncoderOutput,
)
from .errors import (
    APIConnectionError,
    APIRateLimitError,
    AuthenticationError,
    InternalServerError,
)
from typing import Dict, List, Any, Literal, Generator
import modelhub.common.constants as constants
import json
import retrying
from io import TextIOWrapper


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
    timeout: float = 600.0
    """host URL of the Modelhub API"""
    """list of supported models"""
    headers: Dict[str, Any] = {}
    _supported_models: Dict[str, ModelInfo] = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._supported_models = self._get_supported_models()

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
    def supported_models(self) -> Dict[str, ModelInfo]:
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
        response = req_func(
            url, params=params, timeout=self.timeout, headers=self.headers, **kwargs
        )
        if response.status_code == constants.ERR_AUTH_FAILED:
            raise AuthenticationError()
        if response.status_code == constants.ERR_ISE:
            raise InternalServerError(response.text)
        if response.status_code == constants.ERR_API_CONNECTION_ERROR:
            raise APIConnectionError(response.json())
        if response.status_code == constants.ERR_API_RATE_LIMIT:
            raise APIRateLimitError(response.json())
        if response.status_code != 200:
            raise Exception(response.text)
        return response

    def _get_supported_models(self) -> ModelInfoOutput:
        """Get a list of supported models from the Modelhub API"""
        response = self._get(
            self.host + "/models",
        )
        return ModelInfoOutput(**response.json()).models

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

    def n_tokens(self, prompt: str, model: str = "", params={}) -> NTokensOutput:
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
                "model": model,
                "params": params,
            },
            method="post",
        )
        return NTokensOutput(**response.json())

    def chat(
        self,
        prompt: str,
        model: str = "",
        history: List[BaseMessage] = [],
        parameters: ChatParameters = {},
    ) -> TextGenerationOutput:
        model = model or self.model
        if (model not in self.supported_models) or (
            "chat" not in self.supported_models[model].types
        ):
            raise ValueError(f"Model {model} not supported")

        parameters["history"] = convert_messages_to_dicts(history)
        response = self._get(
            self.host + "/chat",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
            method="post",
        )
        out = TextGenerationOutput(**response.json())
        return out

    def stream_chat(
        self,
        prompt: str,
        model: str,
        history: List[BaseMessage] = [],
        parameters: Dict[str, Any] = {},
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        model = model or self.model
        if (model not in self.supported_models) or (
            "chat" not in self.supported_models[model].types
        ):
            raise ValueError(f"Model {model} not supported")

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
            if token.startswith(b"data:"):
                out = TextGenerationStreamOutput(**json.loads(token[5:]))
                if out.code == constants.ERR_API_RATE_LIMIT:
                    raise APIRateLimitError(out)
                if out.code == constants.ERR_ISE:
                    raise InternalServerError(out)
                if out.code == constants.ERR_AUTH_FAILED:
                    raise AuthenticationError(out)
                if out.code == constants.ERR_API_CONNECTION_ERROR:
                    raise APIConnectionError(out)
                if out.code != 200:
                    raise Exception(out)
                yield out

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
        model = model or self.model
        if (model not in self.supported_models) or (
            "embedding" not in self.supported_models[model].types
        ):
            raise ValueError(f"Model {model} not supported")

        response = self._get(
            self.host + "/embedding",
            json={
                "prompt": prompt,
                "model": model,
                "parameters": parameters,
            },
            method="post",
        )
        return EmbeddingOutput(**response.json())

    def cross_embedding(
        self,
        sentences: List[List[str]],
        model: str,
        parameters: CrossEncoderParams = {},
    ) -> CrossEncoderOutput:
        """
        Performs predicts with the CrossEncoder on the given sentence pairs.
        :param sentences: A list of sentence pairs [[Sent1, Sent2], [Sent3, Sent4]]
        """
        model = model or self.model
        if (model not in self.supported_models) or (
            "reranker" not in self.supported_models[model].types
        ):
            raise ValueError(f"Model {model} not supported")
        res = self._get(
            self.host + "/cross_embedding",
            json={
                "sentences": sentences,
                "model": model,
                "parameters": parameters,
            },
            method="post",
        )
        return CrossEncoderOutput(**res.json())

    def transcribe(
        self,
        file: str | TextIOWrapper,
        model: str = "",
        language: str = "",
        temperature: float = 0.0,
    ):
        model = model or self.model
        if (model not in self.supported_models) or (
            "audio" not in self.supported_models[model].types
        ):
            raise ValueError(f"Model {model} not supported")

        if isinstance(file, str):
            file = open(file, "rb")

        session = requests.Session()
        res = session.post(
            url=self.host + "/audio/transcriptions",
            headers=self.headers,
            files={"file": file},
            data={
                "model": model,
                "language": language,
                "temperature": temperature,
            },
        )
        if res.status_code != 200:
            raise Exception(res.text)
        return Transcription(**res.json())


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
