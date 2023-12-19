from pydantic import BaseModel as PydanticBaseModel
from fastapi.responses import JSONResponse
from typing import Dict, Optional, Any, List, Union
import json


class BaseModel(PydanticBaseModel):
    def to_event(self, prefix="data: ") -> str:
        return f"{prefix}{self.json()}\r\n\r\n"

    class Config:
        arbitrary_types_allowed = True


class GenerationParams(BaseModel):
    """
    GenerationParams: Parameters for text generation
    """

    inputs: str
    """inputs: the input text"""
    parameters: Dict[str, Any] = {}
    """parameters: the parameters for the model"""


class TextGenerationStreamToken(BaseModel):
    """TextGenerationStreamToken: A token in the text generation stream"""

    id: int = 0
    """id: the token id"""
    text: str
    """text: the token text"""
    logprob: float = 0
    """logprob: the log probability of the token"""
    special: bool = False
    """special: whether the token is a special token"""


class BaseMessage(BaseModel):
    role: str
    content: str
    kwargs: Dict[str, Any] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = kwargs.pop("role", self.role)
        self.content = kwargs.pop("content", self.content)
        self.kwargs = kwargs

    def dict(self):
        return {"role": self.role, "content": self.content, **self.kwargs}

    def __str__(self):
        return json.dumps(self.dict(), ensure_ascii=False)


class SystemMessage(BaseMessage):
    role: str = "system"


class UserMessage(BaseMessage):
    role: str = "user"


class AIMessage(BaseMessage):
    role: str = "assistant"


class ToolMessage(BaseMessage):
    role: str = "tool"


def convert_messages_to_dicts(messages: List[BaseMessage]) -> List[Dict[str, Any]]:
    """Convert a list of messages to a list of dicts"""
    return [message.dict() for message in messages]


def convert_dicts_to_messages(dicts: List[Dict[str, Any]]) -> List[BaseMessage]:
    """Convert a list of dicts to a list of messages"""
    messages = []
    for d in dicts:
        if d["role"] == "system":
            messages.append(SystemMessage(**d))
        elif d["role"] == "user":
            messages.append(UserMessage(**d))
        elif d["role"] == "assistant":
            messages.append(AIMessage(**d))
        elif d["role"] == "tool":
            messages.append(ToolMessage(**d))
        else:
            messages.append(BaseMessage(**d))
    return messages


class TextGenerationDetails(BaseModel):
    """TextGenerationStreamDetails: Details of the text generation stream"""

    finish_reason: Optional[str] = None
    """finish_reason: the reason for finishing the generation"""
    request_time: Optional[float] = None
    prompt_tokens: Optional[int] = None
    """prompt_tokens: the number of tokens in the prompt"""
    generated_tokens: Optional[int] = None
    """generated_tokens: the number of tokens generated"""
    seed: Optional[int] = None
    """seed: the seed for the generation"""
    tokens: Optional[List[TextGenerationStreamToken]] = None
    """tokens: the tokens in the generation stream"""


class TextGenerationStreamDetails(BaseModel):
    """TextGenerationStreamDetails: Details of the text generation stream"""

    finish_reason: Optional[str] = None
    """finish_reason: the reason for finishing the generation"""
    request_time: Optional[float] = None
    prompt_tokens: Optional[int] = None
    """prompt_tokens: the number of tokens in the prompt"""
    generated_tokens: Optional[int] = None
    """generated_tokens: the number of tokens generated"""
    seed: Optional[int] = None
    """seed: the seed for the generation"""
    tokens: Optional[List[TextGenerationStreamToken]] = None
    """tokens: the tokens in the generation stream"""


class TextGenerationStreamOutput(BaseModel):
    """TextGenerationStreamOutput: Output of the text generation stream"""

    success: bool = True
    token: TextGenerationStreamToken
    """token: the token generated"""
    generated_text: Optional[str] = None
    history: List[Dict[str, Any]] = []
    """generated_text: the generated text"""
    details: Optional[TextGenerationStreamDetails] = None
    """details: the details of the generation stream"""


class TextGenerationOutput(BaseModel):
    """TextGenerationOutput: Output of text generation"""

    success: bool = True
    generated_text: str
    history: List[Dict[str, Any]] = []
    """generated_text: the generated text"""
    details: Optional[TextGenerationStreamDetails] = None
    """details: the details of the generation stream"""


class ErrorMessage(BaseModel):
    """ErrorOutput: Output of text generation"""

    success: bool = False
    err_code: int
    err_msg: str
    """error: the error message"""

    def to_response(self):
        return JSONResponse(self.dict(), status_code=self.err_code)


class EmbeddingOutput(BaseModel):
    """EmbeddingOutput: Output of text embedding"""

    embeddings: List[List[float]]
    """embeddings: the embeddings of the text"""
