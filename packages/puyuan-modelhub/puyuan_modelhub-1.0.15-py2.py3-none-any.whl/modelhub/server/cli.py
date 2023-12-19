from fastapi import FastAPI
from .apis import openai, modelhub
from .lib.config import get_config
from uvicorn import run


def create_local_server(model: str, port: int):
    config = get_config()
    model_config = next((m for m in config.local_models if m.name == model), None)
    if model_config is None:
        raise Exception(f"Model {model} not found in config.yaml")
    config.local_models = [model_config]
    app = FastAPI()
    app.include_router(openai.router)
    app.include_router(modelhub.router)
