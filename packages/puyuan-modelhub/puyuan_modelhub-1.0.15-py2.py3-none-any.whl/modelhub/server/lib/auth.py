from ..apis.types import AuthParams
from .utils import hash_password
from .db import get_mongo_db
from .config import get_config
from fastapi import Request


def get_auth_params(request: Request):
    """Get auth params"""
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if not auth:
        return None
    auth = auth.replace("Bearer ", "")
    if len(auth.split(":", 1)) != 2:
        return None
    user_name, user_password = auth.split(":", 1)
    return AuthParams(user_name=user_name, user_password=user_password)


def check_user_auth(params: AuthParams | None):
    """Check user authentication"""
    users_collection = get_mongo_db()[get_config().db.users_collection]
    if not params:
        return False
    hashed_password = hash_password(params.user_password)
    user = users_collection.find_one({"_id": params.user_name})
    if not user:
        return False
    return user["password"] == hashed_password
