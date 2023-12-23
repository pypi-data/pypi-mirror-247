from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from modelhub.server.models.errors import *
from ...server.models.local.whisper import BaseAudioModel
from openai.types.audio.transcription_create_params import TranscriptionCreateParams
from modelhub.common.types import (
    ErrorMessage,
    StreamErrorOutput,
    ModelInfoOutput,
    NTokensOutput,
    Transcription,
)
import datetime
import os
import hashlib
from ..lib.config import get_config

from ..lib import get_auth_params
from ...server.models.model_factory import get_model_factory
from ..lib import log_to_db_modelhub as log_db
from loguru import logger
from ..models.base import BaseCrossEncoderModel, BaseChatModel
from .types import ChatParams, EmbeddingParams, CrossEncodingParams
from typing import Annotated, Optional
import traceback
import openai

router = APIRouter()


async def _stream_generator(params: ChatParams, request: Request):
    try:
        model = get_model_factory().get(params.model)
    except Exception as e:
        yield StreamErrorOutput(msg=f"model failed to load: {e}").to_event()

    try:
        for token in model.stream(params.prompt, params.parameters):
            yield token.to_event()
        log_db(request, params, token)
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


@router.post("/chat")
async def chat(params: ChatParams, request: Request):
    """Chat with a model"""
    auth = get_auth_params(request)
    logger.info(f"[MODELHUB] user: {auth.user_name} request: {params.model}")

    if params.stream:
        return StreamingResponse(
            _stream_generator(params, request), media_type="text/event-stream"
        )

    start_time = datetime.datetime.now()

    try:
        model = get_model_factory().get(params.model)
    except Exception as e:
        return ErrorMessage(code=404, msg=f"model load failed: {e}").to_response()

    try:
        if "image_path" in params.parameters:
            params.parameters["image_path"] = os.path.join(
                get_config().app.upload_dir, params.parameters["image_path"]
            )
        result = model.chat(params.prompt, params.parameters)
        request_time = datetime.datetime.now() - start_time
        result.details.request_time = request_time.total_seconds()
        log_db(request, params, result)
        return result
    except openai.APIConnectionError as e:
        logger.error(f"OpenAI API connection error: {e}")
        return ErrorMessage(
            code=501, msg=f"OpenAI API connection error: {e}"
        ).to_response()
    except openai.RateLimitError as e:
        logger.error(f"OpenAI API rate limit error: {e}")
        return ErrorMessage(
            code=502, msg=f"OpenAI API rate limit error: {e}"
        ).to_response()
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(tb)
        return ErrorMessage(code=500, msg=tb).to_response()


@router.post("/embedding")
async def embedding(params: EmbeddingParams):
    """Get embeddings from a model"""
    try:
        model = get_model_factory().get(params.model)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"model failed to load: {e}").to_response()

    try:
        return model.get_embeddings(params.prompt, params.parameters)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"Failed to embedding: {e}").to_response()


@router.post("/cross_embedding")
async def cross_embedding(params: CrossEncodingParams):
    """Get embeddings from a model"""
    try:
        model: BaseCrossEncoderModel = get_model_factory().get(params.model)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"model failed to load: {e}").to_response()

    try:
        return model.predict(params.sentences, params.parameters)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"Failed to embedding: {e}").to_response()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        upload_dir = get_config().app.upload_dir
        file_path = os.path.join(upload_dir, file.filename)
        contents = await file.read()
        file_id = hashlib.md5(contents).hexdigest()
        filename = file_id + "." + file.filename.split(".")[-1]
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        return {"status": "success", "file_path": filename}
    except Exception as e:
        return {"error": f"failed to upload: {e}"}


@router.get("/models")
async def get_models():
    """Get all models"""
    return ModelInfoOutput(models=get_model_factory().models)


@router.get("/models/{model_name}")
async def get_model_supported_params(model_name: str):
    """Get supported parameters for a model"""
    return {
        "status": "success",
        "params": get_model_factory().get_supported_params(model_name),
    }


@router.post("/tokens")
async def tokens(params: ChatParams):
    """Get tokens from a model"""
    try:
        model = get_model_factory().get(params.model)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"model failed to load: {e}").to_response()

    try:
        n_tokens = model.n_tokens(params.prompt, params.parameters)
        return NTokensOutput(n_tokens=n_tokens)
    except Exception as e:
        return ErrorMessage(code=500, msg=f"Failed to get tokens: {e}").to_response()


@router.post("/audio/transcriptions")
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
        return ErrorMessage(code=500, msg=f"model failed to load: {e}").to_response()
