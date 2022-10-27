"""This section implements the meta classes for quantcerebro components.
It defines the skeleton of attributes and functionality a class component should implement.
"""
from __future__ import annotations

import logging
from abc import abstractmethod , ABC
from dataclasses import dataclass
from importlib import import_module
from typing import Optional , Dict , Any , Callable , TypeVar

GraphEventEmitter = TypeVar("GraphEventEmitter")
GraphEvent = TypeVar("GraphEvent")
NodeSet = TypeVar("NodeSet")

ImplementedInterfaceType = TypeVar("ImplementedInterfaceType")
RegisteredInterfaceType = TypeVar("RegisteredInterfaceType")
ImplementedHandlerType = TypeVar("ImplementedHandlerType")


class PredecessorTemplate(ABC):
    """
    Predecessor Abstract Class for a scenario component
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """ name of the predecessor scenario component """
        raise NotImplementedError

    @property
    @abstractmethod
    def implemented_interfaces(self) -> Optional[ ImplementedInterfaceType ]:
        """ interface implemented by a Predecessor scenario component """
        raise NotImplementedError

    @property
    @abstractmethod
    def event_emitter(self) -> Optional[ GraphEventEmitter ]:
        """ event emitter """
        raise NotImplementedError

    @property
    @abstractmethod
    def registered_events(self) -> Optional[ Dict[ str , GraphEvent ] ]:
        """ events registered in Predecessor Scenario Component"""
        raise NotImplementedError

    @abstractmethod
    def add_event(self , node_name: str , event_name: str):
        """ create an event to component"""
        raise NotImplementedError

    @abstractmethod
    def get_event(self , node_name: str , event_name: str) -> GraphEvent:
        """get a event by name from a component"""
        raise NotImplementedError

    @abstractmethod
    def register_handler_to_event(self , node_name: str , event_name: str , event_handler: Callable):
        """register event handler to a event of a component"""
        raise NotImplementedError

    @abstractmethod
    def notify_handlers(self , node_name: str , event_name: str , *msg):
        """ for a event of node, notify to it's registered handlers """
        raise NotImplementedError

    @abstractmethod
    def consolidate_implemented_interfaces(self):
        """ manually register implemented interface to a dictionary """
        raise NotImplementedError


class SuccessorTemplate(ABC):
    """
    Successor Abstract Class for a scenario component
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """ name of successor  scenario component"""
        raise NotImplementedError

    @property
    @abstractmethod
    def registered_interfaces(self) -> Optional[ RegisteredInterfaceType ]:
        """ registered interfaces to Successor Scenario component """
        raise NotImplementedError

    @property
    @abstractmethod
    def implemented_event_handlers(self) -> Optional[ ImplementedHandlerType ]:
        """ implemented event handlers """
        raise NotImplementedError

    @abstractmethod
    def register_interface_to_node(self , node_name: str , interface_name: str , interface: Any) -> None:
        """ register a predecessor interface to successor scenario component"""
        raise NotImplementedError

    @abstractmethod
    def consolidate_implemented_handlers(self) -> Dict[ str , Any ]:
        """ manually register implemented handlers to a dictionary"""
        raise NotImplementedError


class ScenarioComponent(PredecessorTemplate , SuccessorTemplate):
    """
    Scenario Component has two child implementation. :class:`.Node` and :class:`.NodeSet`
    Scenario Component is an abstract class that inherents from :class:`.PredecessorTemplate` and :class:`.SuccessorTemplate`
    """

    def __init__(self):
        self.parent: NodeSet = None

    @property
    @abstractmethod
    def name(self) -> str:
        """ Name of Scenario Compoment, by default, it's taken from scenario config"""
        raise NotImplementedError

    @abstractmethod
    def is_nodeset(self) -> bool:
        """ if the current scenario is a nodeset """
        raise NotImplementedError

    def get_nodeset(self , name: Optional[ str ] = None) -> NodeSet:
        """ get a child nodeset by name """
        raise NotImplementedError


@dataclass
class Config:
    """
    Base class for Scenario Component Configurations, there are two child implementations, :class:`.NodeSetConfig` and :class:`.NodeConfig`.
    :param name: name of the config
    :param config_class: the string path to designinated Config Class
    :param parent: not a required param, by default it's None, and set at runtime by scenario config
    """
    name: str
    config_class: str

    def __post_init__(self):
        self.parent = None

    def is_nodeset_config(self) -> bool:
        """is current configuration a nodeset config"""
        return False

    def get_nodeset_config(self , name: str):
        """ get child nodest config by name """
        raise NotImplementedError

