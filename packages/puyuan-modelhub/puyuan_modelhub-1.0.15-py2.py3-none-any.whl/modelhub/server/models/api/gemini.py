from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
)
from ....common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
)
from ...models.base import BaseChatModel
from typing import Optional, Dict, List, Any, Generator, Literal
import google.generativeai as genai
from pydantic import root_validator
from loguru import logger


def convert_dicts_to_glm(d: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    role_map = {"user": "user", "bot": "bot", "system": "model", "assistant": "model"}
    return [
        {"role": role_map.get(m["role"], "model"), "parts": [m["content"]]} for m in d
    ]


class GeminiModel(BaseChatModel):
    api_key: str
    model_name: str = "gemini-pro"
    _model: genai.GenerativeModel = None

    @root_validator(pre=False)
    def configure_genai(cls, values):
        genai.configure(api_key=values["api_key"])
        values["_model"] = genai.GenerativeModel(values["model_name"])
        return values

    def chat(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationOutput:
        history = parameters.pop("history", [])
        history = convert_dicts_to_glm(history) + [{"role": "user", "parts": [prompt]}]
        logger.info(f"history: {history}, parameters: {parameters}")
        try:
            response = self._model.generate_content(history, **parameters)
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise e
        logger.info(f"response: {response.text}")
        return TextGenerationOutput(
            generated_text=response.text,
            details=TextGenerationStreamDetails(
                finish_reason="stop",
            ),
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any] = {}
    ) -> TextGenerationStreamOutput:
        history = parameters.pop("history", [])
        history = convert_dicts_to_glm(history) + [{"role": "user", "parts": [prompt]}]
        response = self._model.generate_content(history, **parameters, stream=True)
        for chunk in response:
            yield TextGenerationStreamOutput(
                token=TextGenerationStreamToken(
                    text=chunk.text,
                )
            )

    def n_tokens(self, prompt: str, parameters: Dict[str, Any]) -> int:
        return self._model.count_tokens(prompt, **parameters)

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any] = {}
    ) -> EmbeddingOutput:
        task_type = parameters.pop("task_type", "retrieval_document")
        title = parameters.pop("title", None)
        if task_type == "retrieval_document" and title is None:
            raise ValueError(
                "The `title` parameter must be specified when `task_type` is `retrieval_document`"
            )
        result = genai.embed_content(
            model="models/embedding-001",
            title=title,
            content=prompt,
            task_type=task_type,
        )
        if isinstance(prompt, str):
            return EmbeddingOutput(embeddings=[result["embedding"]])
        return EmbeddingOutput(embeddings=result["embedding"])
