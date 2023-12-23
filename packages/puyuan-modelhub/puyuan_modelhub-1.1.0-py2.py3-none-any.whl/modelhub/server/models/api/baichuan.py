from modelhub.common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationDetails,
    TextGenerationStreamToken,
)
from ..base import BaseChatModel
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Literal
import requests
import retrying
import os
import json


class BaichuanMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class BaichuanKnowledgeBaseParams(BaseModel):
    ids: List[str]


class BaichuanPostParams(BaseModel):
    model: Literal["Baichuan2-Turbo", "Baichuan2-Turbo-192k"]
    messages: List[BaichuanMessage]
    stream: bool = False
    temperature: float = 0.3
    top_p: float = 0.85
    top_k: int = Field(default=5, ge=0, le=20)
    with_search_enhance: bool = False
    # knowledge_base: BaichuanKnowledgeBaseParams = []

    class Config:
        extra = "forbid"


class BaichuanOutputChoice(BaseModel):
    finish_reason: Literal["stop", "content_filter"]
    index: int
    message: BaichuanMessage


class BaichuanOutputDelta(BaseModel):
    finish_reason: Optional[Literal["stop", "content_filter"]] = None
    index: int
    delta: BaichuanMessage


class BaichuanOutputUsage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class BaichuanOutputCites(BaseModel):
    title: str
    file_id: str
    content: str


class BaichuanOutputKnowledge(BaseModel):
    cites: List[BaichuanOutputCites]


class BaichuanOutput(BaseModel):
    id: str
    created: int = Field(description="unix timestamp")
    choices: List[BaichuanOutputChoice]
    model: str
    object: str = "chat.completion"
    usage: BaichuanOutputUsage
    knowledge_base: Optional[BaichuanOutputKnowledge] = None


class BaichuanStreamOutput(BaseModel):
    id: str
    created: int = Field(description="unix timestamp")
    choices: List[BaichuanOutputDelta]
    model: str
    object: str = "chat.completion"
    knowledge_base: Optional[BaichuanOutputKnowledge] = None


class BaichuanEmbeddingParams(BaseModel):
    model: Literal["Baichuan-Text-Embedding"] = "Baichuan-Text-Embedding"
    input: str | List[str]


def _stream(o: BaichuanStreamOutput) -> TextGenerationStreamOutput:
    return TextGenerationStreamOutput(
        token=TextGenerationStreamToken(text=o.choices[0].delta.content),
        details=TextGenerationDetails(finish_reason=o.choices[0].finish_reason),
    )


def _sync(baichuan_output: BaichuanOutput) -> TextGenerationOutput:
    return TextGenerationOutput(
        generated_text=baichuan_output.choices[0].message.content,
        details=TextGenerationDetails(
            finish_reason=baichuan_output.choices[0].finish_reason,
            prompt_tokens=baichuan_output.usage.prompt_tokens,
            generated_tokens=baichuan_output.usage.completion_tokens,
        ),
    )


class BaichuanModel(BaseChatModel):
    api_key: Optional[str] = os.getenv("BAICHUAN_API_KEY")
    model: Literal["Baichuan2-Turbo", "Baichuan2-Turbo-192k"]
    host: str = "https://api.baichuan-ai.com/v1/chat/completions"
    max_retries: int = 3
    wait_fixed: int = 1000

    @retrying.retry(
        stop_max_attempt_number=max_retries,
        wait_fixed=wait_fixed,
        retry_on_exception=lambda e: isinstance(
            e, requests.exceptions.RequestException
        ),
    )
    def _post(
        self,
        params: BaichuanPostParams | BaichuanEmbeddingParams,
        host: Optional[str] = None,
    ) -> Any:
        return requests.post(
            host or self.host,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=params.dict(),
            stream=params.stream if isinstance(params, BaichuanPostParams) else False,
        )

    def chat(self, prompt: str, parameters: Dict[str, Any]) -> TextGenerationOutput:
        history = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        return _sync(
            BaichuanOutput(
                **self._post(
                    BaichuanPostParams(
                        model=self.model,
                        messages=history,
                        **parameters,
                    )
                ).json()
            )
        )

    def stream(
        self, prompt: str, parameters: Dict[str, Any]
    ) -> TextGenerationStreamOutput:
        history = parameters.pop("history", []) + [{"role": "user", "content": prompt}]
        for line in self._post(
            BaichuanPostParams(
                model=self.model,
                messages=history,
                stream=True,
                **parameters,
            )
        ).iter_lines(delimiter=b"\n\n"):
            if line == b"data: [DONE]":
                return
            if line.startswith(b"data:"):
                yield _stream(BaichuanStreamOutput(**json.loads(line[5:])))

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        embedding_url = "https://api.baichuan-ai.com/v1/embeddings"
        ret = self._post(
            BaichuanEmbeddingParams(input=prompt), host=embedding_url
        ).json()
        return EmbeddingOutput(embeddings=[e["embedding"] for e in ret["data"]])
