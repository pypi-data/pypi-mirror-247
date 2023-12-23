from ....common.types import EmbeddingOutput, CrossEncoderOutput
from ...models.errors import *
from ...models.base import BaseChatModel, BaseCrossEncoderModel
from typing import Generator, Optional, Dict, List, Any
from pydantic import PrivateAttr
from sentence_transformers import SentenceTransformer, CrossEncoder
from modelhub.common.types.encoder import CrossEncoderParams

DEFAULT_SENTENCE_TRANSFORMER_MAX_LENGTH = 512


class CrossEncoderModel(BaseCrossEncoderModel):
    local_model_path: str
    cuda_device: int = 0
    _model: CrossEncoder = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._model = CrossEncoder(
            self.local_model_path,
            max_length=DEFAULT_SENTENCE_TRANSFORMER_MAX_LENGTH,
            device=f"cuda:{self.cuda_device}",
        )

    def predict(
        self, sentences: List[List[str]], parameters: CrossEncoderParams
    ) -> CrossEncoderOutput:
        scores = self._model.predict(sentences, **parameters)
        return CrossEncoderOutput(scores=scores.tolist())


class SentenceTransformerModel(BaseChatModel):
    local_model_path: str
    cuda_device: int = 0
    model: Optional[Any] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.model = SentenceTransformer(self.local_model_path)
            self.model.eval()
        except Exception as e:
            raise ModelLoadError(f"Failed to load Embedding Model: {e}")

    def get_embeddings(
        self, prompt: str | List[str], parameters: Dict[str, Any]
    ) -> EmbeddingOutput:
        prompt = [prompt] if isinstance(prompt, str) else prompt
        try:
            embeddings = self.model.encode(prompt)
        except Exception as e:
            raise ModelGenerateError(f"Failed to generate embeddings: {e}")
        return EmbeddingOutput(embeddings=embeddings.tolist())
