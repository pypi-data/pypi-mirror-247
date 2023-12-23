from ..lib.config import LocalModelConfig, Config, get_config, set_config
import multiprocessing as mp
import requests
from loguru import logger


def check_server_running(model_config: LocalModelConfig):
    url = f"http://127.0.0.1:{model_config.port}/models"
    try:
        r = requests.get(url).json()["models"]
        if model_config.name in r:
            return True
    except:
        return False
    return False


def _start_server(config: Config, model_config: LocalModelConfig):
    config.local_models = [model_config]
    config.api_models = []
    config.app.is_sub_process = True
    config.app.workers = 1
    set_config(config)
    from fastapi import FastAPI

    app = FastAPI()
    from ..apis import modelhub, openai

    app.include_router(modelhub.router)
    app.include_router(openai.router)
    import os

    logger.info(f"starting server at {model_config.port}, PID: {os.getpid()}")
    import uvicorn

    uvicorn.run(app, port=model_config.port)


def start_server(model_config: LocalModelConfig):
    config = get_config()
    p = mp.Process(target=_start_server, args=(config, model_config), daemon=True)
    p.start()
    # wait for server to start
    import time

    time.sleep(5)
    return p
