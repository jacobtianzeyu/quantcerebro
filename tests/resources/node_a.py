from __future__ import annotations

from abc import abstractmethod , ABC
from dataclasses import dataclass
from typing import Dict , Any , TypedDict , Type , Generic , cast

from src.quantcerebro import Node, NodeConfig


class InterfaceA(ABC):
    @abstractmethod
    def interface_method(self):
        raise NotImplementedError


class AModel:
    def __init__(self, attr:str):
        self.attr = attr

    def return_attr(self):
        return self.attr


@dataclass
class AConfig(NodeConfig):
    attr:str

    @classmethod
    def from_dict(cls, config_dict:Dict ) -> AConfig:
        name = config_dict["name"]
        config_class = config_dict["configClass"]
        node_class = config_dict["nodeClass"]
        dependency_tag = name
        attr = config_dict["attr"]
        return cls(name, config_class, node_class, dependency_tag, attr)


class ImplementedInterfaceType(TypedDict,total=False):
    InterfaceA: InterfaceA


class A(Node, InterfaceA):
    def __init__(self, node_config: AConfig):
        super().__init__(node_config)
        self.node_config = cast(AConfig, node_config)
        self.model = cast(AModel, self.model)

    def init_model(self) -> AModel:
        return AModel(self.node_config.attr)

    def interface_method(self):
        return "interface_return_value"

    def consolidate_implemented_interfaces(self):
        super().consolidate_implemented_interfaces()
        self.implemented_interfaces["A.InterfaceA"] = self


if __name__ == "__main__":

    aconfig = AConfig("Aattr")

    a = A(aconfig)
    # a = A(aconfig)
    print(a.model.attr)
    print(a.interface_method())
    print(InterfaceA.__name__)
    a.consolidate_implemented_interfaces()

    a.implemented_interfaces.get("InterfaceA").interface_method()


