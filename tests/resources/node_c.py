from __future__ import annotations

from abc import abstractmethod , ABC
from dataclasses import dataclass
from typing import Dict , Any , cast

from src.quantcerebro import Node , NodeConfig


class CModel:
    def __init__(self, attr:str):
        self.attr = attr

    def return_attr(self):
        return self.attr


@dataclass
class CConfig(NodeConfig):
    attr:str

    @classmethod
    def from_dict(cls, config_dict:Dict ) -> CConfig:
        name = config_dict["name"]
        config_class = config_dict["configClass"]
        node_class = config_dict["nodeClass"]
        dependency_tag = name
        attr = config_dict["attr"]
        return cls(name, config_class, node_class, dependency_tag, attr)


class C(Node):

    def __init__(self, node_config:CConfig):
        super().__init__(node_config)
        self.node_config = cast(CConfig, node_config)
        self.model = cast(CModel, self.model)

    def init_model(self) -> CModel:
        return CModel(self.node_config.attr)

    def event_a_handler(self,msg):
        print(msg)

    def consolidate_implemented_handlers(self):
        super(C, self).consolidate_implemented_handlers()
        self.implemented_event_handlers[""] = ""




