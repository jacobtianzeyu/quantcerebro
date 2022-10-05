from __future__ import annotations

import logging
from abc import ABC , abstractmethod
from typing import Dict , Type , Any , Callable , Set , Mapping
from dataclasses import dataclass

from .event import GraphEventEmitter , GraphEvent


class PredecessorNode(ABC):
    """
    Predecessor Node is an abstract class. It should ONLY be inherited.
    Predecessor Node house the logic for implemented interface and events, and handler registration functionalities
    1) Predecessor Node implements a interface such that a registered successor node can use its functionality.
    2) Predecessor Node defines a event, and successor node's handler is registered to it
    """
    # __slots__ = ("registered_interfaces","event_emitter")
    logger = logging.getLogger(__name__)

    def __init__(self):
        super(PredecessorNode,self).__init__()
        self.event_emitter = GraphEventEmitter()
        self.implemented_interfaces: Dict[ str , Any ] = self._consolidate_implemented_interfaces()
        if not isinstance(self.implemented_interfaces,dict):
            raise TypeError("implemented_interface should be a dictionary")


    @abstractmethod
    def init_model(self, config: NodeConfig):
        raise NotImplementedError

    def add_event(self, event_name:str):
        # self.events[event.name()] = event
        self.event_emitter.create_event(event_name)

    def get_event(self,event_name:str)-> GraphEvent:
        try:
            event = self.event_emitter.events[ event_name ]
        except KeyError:
            raise KeyError("Event Not Found")
        return event

    def register_handler_to_event(self, event_name:str, event_handler:Callable):
        self.event_emitter.add_listener(event_name , event_handler)

    def notify_handlers(self, event_name:str, *msg):

        self.event_emitter.emit(event_name,*msg)

    def _consolidate_implemented_interfaces(self) -> Dict[str, Any]:
        """return a dictionary of implemented of interface"""
        return dict()


class SuccessorNode(ABC):
    """
    SuccessorNode Node is an abstract class. It should not be inherited
    """
    # __slots__ = ("event_handlers","implemented_interfaces")
    logger = logging.getLogger(__name__)

    def __init__(self):
        super(SuccessorNode,self).__init__()
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


class IConfigRetriever(ABC):
    def request(self, name:str) -> NodeConfig:
        raise NotImplementedError


class Node(SuccessorNode, PredecessorNode, IConfigRetriever):
    """
    Node is the presenter for a model.
    Node can't be called on itself, it needs to be inherented.
    """

    def __init__(self, node_config: NodeConfig):
        super(Node,self).__init__()
        self.name = node_config.name
        if not IConfigRetriever.__name__ in self.implemented_interfaces:
            raise KeyError("_consolidate_implemented_interfaces inheritance issue, "
                           "IConfigRetriever should be within, try super()._consolidate_implemented_interfaces()")
        # self.config = node_config
        # self.model = self.init_model(node_config)

    def init_model(self, config: NodeConfig):
        raise NotImplementedError

    def _consolidate_implemented_interfaces(self)-> Dict[str,Any]:
        out = dict()
        out[ IConfigRetriever.__name__ ] = self
        return out

    def _consolidate_implemented_handlers(self) -> Dict[str,Any]:
        raise NotImplementedError

    def request(self, name:str) -> NodeConfig:
        raise NotImplementedError


@dataclass
class NodeConfig:

    name: str

    @classmethod
    def from_file(cls, name: str) -> NodeConfig:
        out = cls(name)
        return out





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