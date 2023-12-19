from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import StreamingResponse
from modelhub.server.models.errors import *
from modelhub.common.types import ErrorMessage
import datetime
import os
import hashlib
from ..lib.config import get_config

from ..lib import get_auth_params
from ...server.models.model_factory import get_model_factory
from ..lib import log_to_db_modelhub as log_db
from loguru import logger
from .types import ChatParams, EmbeddingParams
import traceback
import openai

router = APIRouter()


@router.post("/chat")
async def chat(params: ChatParams, request: Request):
    """Chat with a model"""
    auth = get_auth_params(request)
    logger.info(f"[MODELHUB] user: {auth.user_name} request: {params.model}")
    start_time = datetime.datetime.now()
    # load model
    try:
        model = get_model_factory().get(params.model)
    except ModelNotFoundError as e:
        return ErrorMessage(err_code=404, err_msg=f"model not found: {e}").to_response()
    except Exception as e:
        return ErrorMessage(
            err_code=500, err_msg=f"model failed to load: {e}"
        ).to_response()

    async def stream_generator():
        try:
            for token in model.stream(params.prompt, params.parameters):
                yield token.to_event()
            log_db(request, params, token)
        except Exception as e:
            yield ErrorMessage(err_code=500, err_msg=f"Failed to chat: {e}").to_event()
            return

    if params.stream:
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
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
            err_code=501, err_msg=f"OpenAI API connection error: {e}"
        ).to_response()
    except openai.RateLimitError as e:
        logger.error(f"OpenAI API rate limit error: {e}")
        return ErrorMessage(
            err_code=502, err_msg=f"OpenAI API rate limit error: {e}"
        ).to_response()
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(tb)
        return ErrorMessage(err_code=500, err_msg=tb).to_response()


@router.post("/embedding")
async def embedding(params: EmbeddingParams):
    """Get embeddings from a model"""
    try:
        model = get_model_factory().get(params.model)
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")

    try:
        response = model.get_embeddings(params.prompt, params.parameters)
        return response
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to embedding: {e}")


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
    return {"status": "success", "models": get_model_factory().models}


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
        return ErrorMessage(err_code=500, err_msg=f"model failed to load: {e}")

    try:
        response = model.n_tokens(params.prompt, params.parameters)
        return {"n_tokens": response, "status": "success"}
    except Exception as e:
        return ErrorMessage(err_code=500, err_msg=f"Failed to get tokens: {e}")
