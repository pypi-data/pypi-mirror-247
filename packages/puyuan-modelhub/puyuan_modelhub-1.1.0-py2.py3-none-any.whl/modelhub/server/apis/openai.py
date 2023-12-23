from fastapi import Request, Form, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import Optional, Annotated

from ..models.model_factory import ModelList
from ..models.errors import ModelNotFoundError
from ..models.local.whisper import BaseAudioModel

from loguru import logger
from openai.types.embedding_create_params import EmbeddingCreateParams
from openai.types.audio import Transcription, TranscriptionCreateParams
from ..lib import log_to_db, get_auth_params
from ...server.models.model_factory import get_model_factory
from .types import RequestParams, AuthParams
from ...common.types import ErrorMessage, StreamErrorOutput
from fastapi import APIRouter
import traceback
import openai

router = APIRouter()


@router.get("/v1/models", response_model=ModelList)
async def list_models():
    return get_model_factory().list_models()


async def _stream_generator(auth: AuthParams, req: RequestParams):
    try:
        model = get_model_factory().get(req["model"])
    except Exception as e:
        yield StreamErrorOutput(msg=f"model failed to load: {e}").to_event()

    try:
        res = []
        for token in model.openai_chat(req):
            res.append(token)
            yield f"data: {token.json()}\r\n\r\n"
        log_to_db(auth.user_name, req["model"], req, res)
    except openai.APIConnectionError as e:
        logger.error(f"OpenAI API connection error: {e}")
        yield StreamErrorOutput(
            code=501, msg=f"OpenAI API connection error: {e}"
        ).to_event()
        return
    except openai.RateLimitError as e:
        logger.error(f"OpenAI API rate limit error: {e}")
        yield StreamErrorOutput(
            code=502, msg=f"OpenAI API rate limit error: {e}"
        ).to_event()
        return
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(tb)
        yield StreamErrorOutput(code=500, msg=tb).to_event()
        return


@router.post("/v1/chat/completions")
async def chat_completion(
    req: RequestParams,
    request: Request,
):
    auth = get_auth_params(request)
    req["stream"] = req.get("stream", False)
    for message in req["messages"]:
        if "function_call" in message and not message["function_call"]:
            message.pop("function_call")

    logger.info(f"[OPENAI] user: {auth.user_name} request: {req['model']}")
    if req["stream"]:
        return StreamingResponse(
            _stream_generator(auth, req), media_type="text/event-stream"
        )

    try:
        model = get_model_factory().get(req["model"])
    except ModelNotFoundError as e:
        logger.error(f"model not found: {e}")
        return ErrorMessage(code=404, msg=f"model not found: {e}").to_response()

    try:
        res = model.openai_chat(req)
        log_to_db(auth.user_name, req["model"], req, res)
        return res
    except Exception:
        tb = traceback.format_exc()
        logger.error(tb)
        return ErrorMessage(code=500, msg=tb).to_response()


@router.post("/v1/audio/transcriptions")
async def transciption(
    file: Annotated[UploadFile, File()],
    model: Annotated[str, Form()],
    language: Annotated[Optional[str], Form()] = None,
    temperature: Annotated[Optional[float], Form()] = None,
):
    req = TranscriptionCreateParams(
        file=await file.read(), model=model, language=language, temperature=temperature
    )
    logger.info(f"transcription request: {req['model']}, {file.filename}")
    try:
        model: BaseAudioModel = get_model_factory().get(model)
        return model.transcribe(req)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"model failed to load: {e}")


@router.post("/v1/embeddings")
async def embeddings(params: EmbeddingCreateParams):
    try:
        model = get_model_factory().get(params["model"])
    except Exception as e:
        return ErrorMessage(code=500, msg=f"model failed to load: {e}").to_response()
    try:
        res = model.get_embeddings_openai(params)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"Failed to embedding: {e}").to_response()
    return res
