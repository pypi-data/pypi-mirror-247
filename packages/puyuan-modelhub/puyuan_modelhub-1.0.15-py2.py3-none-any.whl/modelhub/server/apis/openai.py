from fastapi import Request, Form, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import Optional, Annotated

from ...common.types import ErrorMessage
from ..models.model_factory import ModelList
from ..models.errors import ModelNotFoundError

from loguru import logger
from openai.types.embedding_create_params import EmbeddingCreateParams
from openai.types.audio import Transcription, TranscriptionCreateParams
from ..lib import log_to_db, get_auth_params
from ...server.models.model_factory import get_model_factory
from .types import RequestParams

from fastapi import APIRouter
import traceback

router = APIRouter()


@router.get("/v1/models", response_model=ModelList)
async def list_models():
    return get_model_factory().list_models()


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
    try:
        model = get_model_factory().get(req["model"])
    except ModelNotFoundError as e:
        logger.error(f"model not found: {e}")
        return ErrorMessage(err_code=404, err_msg=f"model not found: {e}")

    def stream_generator():
        res = []
        try:
            for token in model.openai_chat(req):
                res.append(token)
                yield f"data: {token.json()}\r\n\r\n"
            log_to_db(auth.user_name, req["model"], req, res)
        except Exception as e:
            logger.info("stream not implemented")
            yield ErrorMessage(err_code=500, err_msg=str(e)).to_event()
            return

    try:
        logger.info(f"request: {req}")
        if req["stream"] == True:
            return StreamingResponse(stream_generator(), media_type="text/event-stream")
        else:
            res = model.openai_chat(req)
            log_to_db(auth.user_name, req["model"], req, res)
            logger.info(f"generated result: {res.choices[0].message.content}")
            return res
    except Exception:
        tb = traceback.format_exc()
        logger.error(tb)
        return ErrorMessage(err_code=500, err_msg=tb).to_response()


@router.post("/v1/audio/transcriptions")
async def transciption(
    file: Annotated[UploadFile, File()],
    model: Annotated[str, Form()],
    language: Annotated[Optional[str], Form()] = None,
    temperature: Annotated[Optional[float], Form()] = None,
):
    logger.info(f"transcription request: {model}, {file.filename}")
    req = TranscriptionCreateParams(
        file=await file.read(), model=model, language=language, temperature=temperature
    )
    logger.info(f"transcription request: {req['model']}, {file.filename}")
    model = get_model_factory().get(model)
    text = model.transcribe(req)
    return Transcription(text=text)


@router.post("/v1/embeddings")
async def embeddings(params: EmbeddingCreateParams):
    try:
        model = get_model_factory().get(params["model"])
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")
    try:
        res = model.get_embeddings_openai(params)
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to embedding: {e}")
    return res
