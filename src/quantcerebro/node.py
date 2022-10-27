"""

"""
# standard lib imports
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict , TypeVar , Optional

# Local application/library specific imports.
from .event import GraphEventEmitter , GraphEvent
from .meta import ScenarioComponent , ImplementedInterfaceType , RegisteredInterfaceType , ImplementedHandlerType , \
    Config

# 3rd-party imports
...

ModelType = TypeVar("ModelType")
NodeSet = TypeVar("NodeSet")


class Node(ScenarioComponent):

    def __init__(self , node_config: NodeConfig):
        super(Node , self).__init__()
        self.node_config = node_config
        self._imp_interface_map = None
        self._imp_handler_map = None
        self._emitter = GraphEventEmitter()
        self._reg_interfaces = dict()
        self.model: ModelType = self.init_model()

    @property
    def name(self) -> str:
        return self.node_config.name

    @property
    def dependency_tag(self) -> str:
        return self.node_config.dependency_tag

    @property
    def implemented_interfaces(self) -> ImplementedInterfaceType:  # Dict[str, Type]
        if self._imp_interface_map is None:
            raise Exception(f"Node:{self.name}'s consolidate_implemented_interfaces not called")
        return self._imp_interface_map

    @property
    def implemented_event_handlers(self) -> ImplementedHandlerType:
        if self._imp_handler_map is None:
            raise Exception(f"Node:{self.name}'s consolidate_event_handlers not called")
        return self._imp_handler_map

    @property
    def event_emitter(self) -> GraphEventEmitter:
        return self._emitter

    @property
    def registered_events(self) -> Dict[ str , GraphEvent ]:
        return self._emitter.events

    @property
    def registered_interfaces(self) -> RegisteredInterfaceType:
        return self._reg_interfaces

    def init_model(self, *args) -> ModelType:
        raise NotImplementedError

    def is_nodeset(self) -> bool:
        return False

    def get_nodeset(self , name: Optional[ str ] = None) -> NodeSet:
        raise NotImplementedError

    def add_event(self , node_name: str , event_name: str):
        if self.name == node_name:
            self.event_emitter.create_event(event_name)

    def get_event(self , node_name: str , event_name: str) -> GraphEvent:
        if self.name == node_name:
            try:
                out = self.event_emitter.events[ event_name ]
                return out
            except KeyError as exc:
                raise exc
        raise Exception(f"node name mismatch {node_name} vs {self.name}")

    def register_interface_to_node(self , node_name: str , interface_name: str , interface):
        if self.name == node_name:
            self.registered_interfaces[ interface_name ] = interface

    def register_handler_to_event(self , node_name: str , event_name , handler):
        if self.name == node_name:
            self.event_emitter.add_listener(event_name , handler)

    def notify_handlers(self , node_name: str , event_name: str , *msg):
        if self.name == node_name:
            self.event_emitter.get_event(event_name).emit(*msg)

    def consolidate_implemented_handlers(self):
        """keep implemented handlers into one dictionary"""
        self._imp_handler_map = dict()

    def consolidate_implemented_interfaces(self):
        """keep implemented interface into one dictionary"""
        self._imp_interface_map = dict()


@dataclass
class NodeConfig(Config):
    node_class: str
    dependency_tag: str

    @classmethod
    def from_dict(cls , config_dict: Dict) -> NodeConfig:
        name = config_dict[ "name" ]
        node_config_class = config_dict[ "configClass" ]
        node_class = config_dict[ "nodeClass" ]
        return cls(name , node_config_class , node_class , name)

    def get_nodeset_config(self , name: str):
        raise NotImplementedError("this is a node config")
