from __future__ import annotations

from abc import abstractmethod , ABC
from dataclasses import dataclass
from typing import Dict , Any , TypedDict , Type , cast

from src.quantcerebro import Node , NodeConfig


@dataclass
class BEvent:
    msg: str


class BModel:
    def __init__(self, attr:str):
        self.attr = attr

    def return_attr(self):
        return self.attr

@dataclass
class BConfig(NodeConfig):
    attr:str

    @classmethod
    def from_dict(cls, config_dict:Dict ) -> BConfig:
        name = config_dict["name"]
        config_class = config_dict["configClass"]
        node_class = config_dict["nodeClass"]
        dependency_tag = name
        attr = config_dict["attr"]
        return cls(name, config_class, node_class, dependency_tag, attr)


class RegisteredInterfaceType(TypedDict):
    InterfaceA: Type[InterfaceA]


class B(Node):
    def __init__(self, node_config: BConfig):
        super().__init__(node_config)
        self.node_config = cast(BConfig, node_config)
        self.model = cast(BModel, self.model)

    def init_model(self) -> BModel:
        return BModel(self.node_config.attr)





