from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Type , Any

import src.quantcerebro.meta as meta


@dataclass
class EdgeConfig:
    pred: str
    succ: str
    edge_dataclass: str
    edge_type: str


@dataclass(frozen=True)
class Dependency:
    logger = logging.getLogger(__name__)
    pred_node: meta.PredecessorTemplate
    succ_node: meta.SuccessorTemplate

    def __post_init__(self):
        self.register_dependency()

    def register_dependency(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class EventDependency(Dependency):
    event_data_class: Any

    def register_dependency(self):

        # event_name = self.event_data_class.__name__
        event_name = ".".join([ self.pred_node.__class__.__name__ , self.event_data_class.__name__ ])

        if event_name not in self.pred_node.registered_events:
            self.logger.info(f"event<{event_name}> doesn't exist, create event")
            self.pred_node.add_event(self.pred_node.name , event_name)

        # register child handler to parent event
        try:
            succ_handler = self.succ_node.implemented_event_handlers[ event_name ]
            self.pred_node.register_handler_to_event(self.pred_node.name , event_name , succ_handler)
        except KeyError as exc:
            raise exc

        self.logger.info(f"{self.succ_node.name}'s handler<{event_name}> "
                         f"is registered to {self.pred_node.name}")


@dataclass(frozen=True)
class CallableDependency(Dependency):
    interface_data_class: Type

    def register_dependency(self):
        # interface_name = self.interface_data_class.__name__
        interface_name = ".".join([ self.pred_node.__class__.__name__ , self.interface_data_class.__name__ ])
        try:
            pred_interface = self.pred_node.implemented_interfaces[ interface_name ]
            self.succ_node.register_interface_to_node(self.succ_node.name , interface_name , pred_interface)
        except KeyError as exc:
            raise exc

        self.logger.info(
            f"{self.succ_node}'s implemented_interface<{interface_name}> "
            f"is registered to {self.pred_node.name}")
