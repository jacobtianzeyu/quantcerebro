from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Type, Any, TypeVar


from node import Node , SuccessorNode , PredecessorNode


@dataclass(frozen=True)
class Dependency:
    logger = logging.getLogger(__name__)
    pred_node: PredecessorNode
    succ_node: SuccessorNode

    def __post_init__(self):
        self.register_dependency()

    def register_dependency(self) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class EventDependency(Dependency):

    event_data_class: Any

    def register_dependency(self):

        event_name = self.event_data_class.__name__

        if event_name not in self.pred_node.event_emitter.events:
            self.logger.info(f"event<{event_name}> doesn't exist, create event")
            self.pred_node.add_event(event_name)

        # register child handler to parent event
        self.pred_node.register_handler_to_event(event_name, self.succ_node.event_handlers[event_name])

        self.logger.info(f"{self.succ_node.name}'s handler<{event_name}> "
                         f"is registered to {self.pred_node.name}")


@dataclass(frozen=True)
class CallableDependency(Dependency):

    interface_data_class: Type

    def register_dependency(self):
        interface_name = self.interface_data_class.__name__
        self.succ_node.register_interface_to_node(interface_name , self.pred_node.implemented_interfaces[interface_name])

        self.logger.info(
            f"{self.succ_node}'s implemented_interface<{interface_name}> "
            f"is registered to {self.pred_node.name}")

