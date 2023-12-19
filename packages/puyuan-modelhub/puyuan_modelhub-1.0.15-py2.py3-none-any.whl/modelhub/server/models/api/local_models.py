from openai._streaming import Stream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from ....common.types import (
    EmbeddingOutput,
    TextGenerationOutput,
    TextGenerationStreamOutput,
    TextGenerationStreamToken,
    TextGenerationStreamDetails,
)
from ...models.errors import *
from ...models.base import BaseChatModel
from typing import Generator, Optional, Dict, List, Any
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
import json
import os
from ...lib.utils import make_completion, make_chunk
