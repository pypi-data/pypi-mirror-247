from typing import Any, Dict, List

from openai._streaming import Stream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
)
from ..base import BaseChatModel
from ....client.client import ModelhubClient
from pydantic import root_validator


class ModelhubModel(BaseChatModel):
    host: str = "http://127.0.0.1"
    user_name: str = ""
    user_password: str = ""
    model_name: str

    _client: ModelhubClient = None

    @root_validator(pre=False)
    def init_client(cls, values):
        values["_client"] = ModelhubClient(
            host=values["host"],
            user_name=values["user_name"],
            user_password=values["user_password"],
        )
        return values

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        history = parameters.pop("history", [])
        return TextGenerationOutput(
            **self._client.chat(
                prompt,
                self.model_name,
                history,
                parameters,
            )
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        history = parameters.pop("history", [])
        for token in self._client.stream_chat(
            prompt,
            self.model_name,
            history,
            parameters,
        ):
            yield TextGenerationStreamOutput(**token)

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        return super().openai_chat(req)

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        return self._client.get_embeddings(prompt, self.model_name, parameters)
