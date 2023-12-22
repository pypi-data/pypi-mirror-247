from ....common.types import EmbeddingOutput
from ...models.errors import *
from ...models.base import BaseChatModel
from typing import Generator, Optional, Dict, List, Any
from sentence_transformers import SentenceTransformer


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
