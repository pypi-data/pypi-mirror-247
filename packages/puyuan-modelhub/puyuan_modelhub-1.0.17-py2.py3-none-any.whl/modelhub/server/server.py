from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from modelhub.server.models.errors import *
import uvicorn
from contextlib import asynccontextmanager
import torch
from .lib import get_auth_params, check_user_auth
from .lib.config import get_config
from .apis import openai, modelhub


@asynccontextmanager
async def lifespan(app: FastAPI):  # collects GPU memory
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


# setup app
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def validate_token(request: Request, call_next):
    """Validate token"""
    authorized = check_user_auth(get_auth_params(request))
    if not authorized:
        return Response(status_code=401, content="Unauthorized")
    return await call_next(request)


app.include_router(openai.router)
app.include_router(modelhub.router)


def start_server(config_path: str = "config.yaml"):
    """Start the server"""
    config = get_config(config_path).app
    uvicorn.run(
        "modelhub.server.server:app",
        host=config.host,
        port=config.port,
        workers=config.workers,
    )


if __name__ == "__main__":
    start_server()
