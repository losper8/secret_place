from typing import Dict, List, Optional

import confuse
import pydantic

from loguru import logger

from distributor.common.utilies import Singleton


class ApiParams(pydantic.BaseModel):
    host: str
    port: int
    schema: str = 'http'


class EmbsParams(ApiParams):
    emb_name: str


class LogParams(pydantic.BaseModel):
    level: pydantic.constr(min_length=1) = 'INFO'
    output_file: Optional[str]


class QueueParams(pydantic.BaseModel):
    maxsize: int
    retry_attempts: int


class ConfigParams(pydantic.BaseModel):
    api: ApiParams
    containers: List[EmbsParams]
    queue: QueueParams
    log: LogParams


class Config(metaclass=Singleton):
    def __init__(self, data: Optional[Dict] = None):
        try:
            cfg = self._load(data)
            self._cfg = ConfigParams.parse_obj(cfg)
        except pydantic.ValidationError as e:
            logger.error(f'there is an error while parsing {e}')

    def _load(self, data):
        if isinstance(data, str):
            loader = confuse.YamlSource
        elif isinstance(data, str):
            loader = confuse.YamlSource
        else:
            raise Exception("Invalid config format")

        source = loader(data)
        view = confuse.RootView([source])
        return view.get(self.template())

    @property
    def api(self):
        return self._cfg.api

    @property
    def containers(self):
        return self._cfg.containers

    @property
    def log(self):
        return self._cfg.log

    def _containers_template(self):
        return confuse.Optional({
            "host": confuse.String(),
            "port": confuse.Integer(),
            "schema": confuse.String(),
            "emb_name": confuse.String()
        }
    )

    def template(self):
        return {
            "api": {
                "host": confuse.String(),
                "port": confuse.Integer(),
                "schema": confuse.String()
            },
            "containers": confuse.Sequence(self._containers_template()),
            "queue": {
                "maxsize": confuse.Integer(),
                "retry_attempts": confuse.Integer()
            },
            "log": {
                "level": confuse.String(),
                "output_file": confuse.Optional(str)
            }
        }