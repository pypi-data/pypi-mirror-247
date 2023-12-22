import hashlib
import time
import uuid
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice, ChoiceDelta
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionMessage,
)
from openai.types.chat.chat_completion import Choice
import torch
import os


def torch_gc(device: int = 0):
    if torch.cuda.is_available():
        with torch.cuda.device(device):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


def gpu_env(device: int | str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if isinstance(device, str):
                os.environ["CUDA_VISIBLE_DEVICES"] = device
            res = func(*args, **kwargs)
            if isinstance(device, str):
                os.environ["CUDA_VISIBLE_DEVICES"] = ""
            return res

        return wrapper

    return decorator


def make_completion(res, model):
    return ChatCompletion(
        id=uuid.uuid4().hex,
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(role="assistant", content=res),
            )
        ],
        object="chat.completion",
        created=int(time.time()),
        model=model,
    )


def make_chunk(res_delta, model):
    return ChatCompletionChunk(
        id=uuid.uuid4().hex,
        choices=[
            ChunkChoice(
                delta=ChoiceDelta(
                    content=res_delta,
                    role="assistant",
                ),
                finish_reason=None,
                index=0,
            )
        ],
        object="chat.completion.chunk",
        created=int(time.time()),
        model=model,
    )


def hash_password(password: str):
    """
    Hash a password"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
