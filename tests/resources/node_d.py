from __future__ import annotations

from abc import abstractmethod , ABC
from dataclasses import dataclass
from typing import Dict , Any , cast

from resources.node_b import BEvent
from src.quantcerebro import Node , NodeConfig


class DModel:
    def __init__(self, attr: str):
        self.attr = attr

    def return_attr(self):
        return self.attr


@dataclass
class DConfig(NodeConfig):
    attr: str

    @classmethod
    def from_dict(cls, config_dict:Dict ) -> DConfig:
        name = config_dict["name"]
        config_class = config_dict["configClass"]
        node_class = config_dict["nodeClass"]
        dependency_tag = name
        attr = config_dict["attr"]
        return cls(name, config_class, node_class, dependency_tag, attr)

class D(Node):

    def __init__(self, node_config:DConfig):
        super().__init__(node_config)
        self.node_config = cast(DConfig, node_config)
        self.model = cast(DModel, self.model)
        self.event_value = None

    def init_model(self) -> DModel:
        return DModel(self.node_config.attr)

    def handler(self, msg):
        self.event_value = msg

    def consolidate_implemented_handlers(self):
        super().consolidate_implemented_handlers()
        self.implemented_event_handlers["B.BEvent"] = self.handler
