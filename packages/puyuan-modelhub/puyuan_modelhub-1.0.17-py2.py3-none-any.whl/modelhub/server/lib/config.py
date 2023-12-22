from pydantic import BaseModel
from typing import Dict, Optional, List, Union, Any, Literal
from loguru import logger
import os


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 34211
    workers: int = 1
    is_sub_process: bool = False
    upload_dir: str = "/tmp/modelhub/upload"


class ModelConfig(BaseModel):
    name: str
    model_class: str
    model_kwargs: Optional[Dict[str, Any]] = {}
    chat_params: Optional[Dict[str, Any]] = {}
    model_types: Optional[
        List[Union[Literal["chat"], Literal["embedding"], Literal["audio"]]]
    ] = ["chat"]


class LocalModelConfig(ModelConfig):
    port: int


class DBConfig(BaseModel):
    mongo_url: str
    mongo_db: str
    messages_collection: str = "messages"
    openai_collection: str = "openai"
    users_collection: str = "users"


class DashboardConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 7860
    user: str
    password: str


class LoggerConfig(BaseModel):
    level: str = "INFO"
    dir: str = "/tmp/log/modelhub/server.log"


class Config(BaseModel):
    logger: LoggerConfig
    env: Optional[Dict[str, str]] = {}
    db: DBConfig
    app: AppConfig
    api_models: Optional[List[ModelConfig]] = []
    local_models: Optional[List[LocalModelConfig]] = []
    dashboard: Optional[DashboardConfig] = None

    @classmethod
    def from_yaml(cls, path: str):
        import yaml

        with open(path, "r") as f:
            return cls(**yaml.safe_load(f))


_config = None


def set_config(config: Config):
    global _config
    _config = config
    for k, v in _config.env.items():
        if k not in _config:
            os.environ[k] = v
    logger.add(_config.logger.dir, level=_config.logger.level)
    logger.info(f"Config setted, PID: {os.getpid()}")


def get_config(config_path: str = "config.yml") -> Config:
    global _config
    if _config is None:
        _config = Config.from_yaml(config_path)
        for k, v in _config.env.items():
            if k not in _config:
                os.environ[k] = v
        logger.add(_config.logger.dir, level=_config.logger.level)
        logger.info(f"Loaded config from {config_path}, PID: {os.getpid()}")
    return _config
