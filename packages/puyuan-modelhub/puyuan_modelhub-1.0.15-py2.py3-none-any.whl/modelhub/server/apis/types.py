from pydantic import BaseModel
from typing import Dict, Any, List, Optional, Union
from typing_extensions import TypedDict
from openai.types.chat import (
    ChatCompletionMessageParam,
    completion_create_params,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)


class AuthParams(BaseModel):
    """AuthParams: Parameters for authentication"""

    user_name: str
    user_password: str


class ChatParams(BaseModel):
    """ChatParams: Parameters for chat"""

    prompt: str
    model: str
    stream: bool = False
    parameters: Dict[str, Any] = {}


class TokensParams(BaseModel):
    """TokensParams: Parameters for tokens"""

    prompt: str
    model: str
    parameters: Dict[str, Any] = {}


class EmbeddingParams(BaseModel):
    """EmbeddingParams: Parameters for embedding"""

    prompt: str | List[str]
    model: str
    parameters: Dict[str, Any] = {}


class RequestParams(TypedDict, total=False):
    messages: List[ChatCompletionMessageParam]
    model: str
    frequency_penalty: Optional[float]
    function_call: Optional[completion_create_params.FunctionCall]
    functions: Optional[List[completion_create_params.Function]]
    logit_bias: Optional[Dict[str, int]]
    max_tokens: Optional[int]
    n: Optional[int]
    presence_penalty: Optional[float]
    response_format: Optional[completion_create_params.ResponseFormat]
    seed: Optional[int]
    stop: Optional[Union[str, List[str]]]
    stream: Optional[bool]
    temperature: Optional[float]
    tool_choice: Optional[ChatCompletionToolChoiceOptionParam]
    tools: Optional[List[ChatCompletionToolParam]]
    top_p: Optional[float]
    user: Optional[str]
