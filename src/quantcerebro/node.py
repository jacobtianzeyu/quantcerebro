from __future__ import annotations

import logging
from abc import ABC , abstractmethod
from typing import Dict , Type , Any , Callable , Set , Mapping
from dataclasses import dataclass

from event import EventEmitter


class PredecessorNode(ABC):
    # __slots__ = ("registered_interfaces","event_emitter")
    logger = logging.getLogger(__name__)

    def __init__(self):
        super(PredecessorNode,self).__init__()
        self.name = ""
        self.implemented_interfaces: Dict[ str , SuccessorNode ] = dict()
        self.event_emitter = EventEmitter()
        self._consolidate_implemented_interfaces()

    @abstractmethod
    def init_model(self, config: NodeConfig):
        raise NotImplementedError

    def add_event(self, event_name:str):
        # self.events[event.name()] = event
        self.event_emitter.create_event(event_name)

    def register_handler_to_event(self, event_name:str, event_handler:Callable):
        # self.events[event_name] += event_handler
        self.event_emitter.add_listener(event_name , event_handler)

    def get_event(self,event_name:str):
        return self.event_emitter.events[event_name]

    def notify_handlers(self, event_name:str, msg: Any):
        # for k, v in self.event_emitter.events.items():
        #     if msg.__class__ == v:
        #         v.emit(msg)
        self.event_emitter.emit(event_name,msg)

    @abstractmethod
    def _consolidate_implemented_interfaces(self) -> None:
        raise NotImplementedError


class SuccessorNode(ABC):
    # __slots__ = ("event_handlers","implemented_interfaces")
    logger = logging.getLogger(__name__)

    def __init__(self):
        super(SuccessorNode,self).__init__()
        self.name = ""
        self.implemented_event_handlers: Dict[ str , Callable ] = dict()
        self.registered_interfaces: Dict[str, Any] = dict()
        self._consolidate_implemented_handlers()

    @abstractmethod
    def init_model(self , config: NodeConfig):
        raise NotImplementedError

    def register_interface_to_node(self, interface_name:str, interface:Any):
        self.registered_interfaces[interface_name] = interface

    @abstractmethod
    def _consolidate_implemented_handlers(self):
        raise NotImplementedError


class Node(SuccessorNode, PredecessorNode):
    """
    Node is the presenter for a model.
    Node can't be called on itself, it needs to be inherented.
    """

    def __init__(self, node_config: NodeConfig):
        super(Node,self).__init__()
        self.name = node_config.name
        # self.config = node_config
        # self.model = self.init_model(node_config)

    def init_model(self, config: NodeConfig):
        raise NotImplementedError

    def _consolidate_implemented_interfaces(self) -> None:
        raise NotImplementedError

    def _consolidate_implemented_handlers(self) -> None:
        raise NotImplementedError


@dataclass
class NodeConfig:

    name: str

    @classmethod
    def from_file(cls, name: str) -> NodeConfig:
        out = cls(name)
        return out


class IConfigRetriever(ABC):
    def request(self, name:str):
        raise NotImplementedError


class NodeConfigManager:
    """
    todo:
        load node configs to nodeconfig manager, node config manager has a link to all nodes by default, and pushes the config to node.
        there should be a centralised timer.
        This config manager is to solve a usecase of change of config due to schedule...
        This config manager has a interface that each node can call whenever they want
        all nodes implements IConfigRetriever by default and all nodes by default is linked to NodeConfigManager
    """
    def __init__(self):
        self.configs = dict()

    def request(self, name:str):
        ...