from typing import Any, Dict, List, Generator

from openai._streaming import Stream
from openai.types.audio.transcription_create_params import TranscriptionCreateParams
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from modelhub.common.types import (
    CrossEncoderOutput,
    CrossEncoderParams,
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    Transcription,
)
from ..base import BaseChatModel, BaseCrossEncoderModel
from ..local.whisper import BaseAudioModel
from ....client.client import ModelhubClient
from pydantic import root_validator


class ModelhubModel(BaseChatModel, BaseAudioModel, BaseCrossEncoderModel):
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
        return self._client.chat(
            prompt,
            self.model_name,
            history,
            parameters,
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> Generator[TextGenerationStreamOutput, None, None]:
        history = parameters.pop("history", [])
        yield from self._client.stream_chat(
            prompt,
            self.model_name,
            history,
            parameters,
        )

    def openai_chat(
        self, req: CompletionCreateParams
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        return super().openai_chat(req)

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        return self._client.get_embeddings(prompt, self.model_name, parameters)

    def transcribe(self, req: TranscriptionCreateParams) -> Transcription:
        return self._client.transcribe(
            req["file"], req["model"], req["language"], req["temperature"]
        )

    def predict(
        self, sentences: List[List[str]], parameters: CrossEncoderParams
    ) -> CrossEncoderOutput:
        return self._client.cross_embedding(sentences, self.model_name, parameters)
