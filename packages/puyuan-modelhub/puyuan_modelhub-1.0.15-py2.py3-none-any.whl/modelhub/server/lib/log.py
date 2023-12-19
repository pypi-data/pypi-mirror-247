import uuid
from typing import List
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    CompletionCreateParams,
)
from pymongo.collection import Collection
from ..apis.types import ChatParams
import datetime
from .db import get_mongo_db
from .auth import get_auth_params
from .config import get_config
from fastapi import Request


def log_to_db(
    user_id: str,
    model_id: str,
    req: CompletionCreateParams,
    res: ChatCompletion | List[ChatCompletionChunk],
    db: Collection = get_mongo_db()[get_config().db.openai_collection],
):
    """Log a request/response pair to the database."""
    try:
        if isinstance(res, ChatCompletion):
            res = res.dict()
        elif isinstance(res, list):
            res = [c.dict() for c in res]
        result = db.insert_one(
            {
                "user_id": user_id,
                "model_id": model_id,
                "req": req,
                "res": res,
                "created": datetime.datetime.now(),
            }
        )
    except Exception as e:
        print("Error logging to db:", e)
        return None
    return result.inserted_id


def log_to_db_modelhub(
    req: Request,
    params: ChatParams,
    response,
    db: Collection = get_mongo_db()[get_config().db.messages_collection],
):
    """Save a message to the database"""
    try:
        auth = get_auth_params(req)
        result = db.insert_one(
            {
                "message_id": str(uuid.uuid4()),
                "user_id": auth.user_name,
                "model": params.model,
                "prompt": params.prompt,
                "stream": params.stream,
                "parameters": params.parameters,
                "response": response.dict(),
                "created_time": datetime.datetime.now(),
            }
        )
    except Exception as e:
        print(f"Failed to save message: {e}")
        return None
    return result.inserted_id
