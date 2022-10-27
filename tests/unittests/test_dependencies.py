from typing import Dict , Any , Callable , Optional

import pytest
from pytest_mock import MockFixture

from src.quantcerebro import GraphEvent
from src.quantcerebro.event import GraphEventEmitter
from src.quantcerebro.meta import PredecessorTemplate , SuccessorTemplate
from src.quantcerebro.dependencies import Dependency, CallableDependency, EventDependency


@pytest.fixture
def predecessor_node(interface_class) -> PredecessorTemplate:
    class PNode(PredecessorTemplate, interface_class):

        @property
        def name(self) -> str:
            pass

        @property
        def implemented_interfaces(self) -> Optional[ Dict[ str , Any ] ]:
            pass

        @property
        def event_emitter(self) -> Optional[ Dict[ str , Any ] ]:
            pass

        def add_event(self , node_name: str , event_name: str):
            pass

        def get_event(self , node_name: str , event_name: str) -> GraphEvent:
            pass

        def register_handler_to_event(self , node_name: str , event_name: str , event_handler: Callable):
            pass

        def notify_handlers(self , node_name: str , event_name: str , *msg):
            pass

        def consolidate_implemented_interfaces(self) -> Dict[ str , Any ]:
            pass

        def init_model(self,config):
            ...

    return PNode()


@pytest.fixture
def successor_node() -> SuccessorTemplate:
    class SNode(SuccessorTemplate):
        def _consolidate_implemented_handlers(self):
            pass

        def init_model(self,config):
            ...

    return SNode()


@pytest.fixture
def event_data_class():
    class EventDataClass:
        ...

    return EventDataClass


@pytest.fixture
def interface_class():
    class InterfaceClass:
        def interface_func(self, x):
            return x

    return InterfaceClass


def test_register_dependency(predecessor_node, successor_node):
    with pytest.raises(NotImplementedError):
        a = Dependency(predecessor_node,successor_node)


def test_event_register_dependency_missing_handler(predecessor_node,successor_node, event_data_class):
    with pytest.raises(KeyError):
        a = EventDependency(predecessor_node,successor_node,event_data_class)


def test_event_register_dependency(mocker:MockFixture, predecessor_node,successor_node, event_data_class):
    event_key = f"{predecessor_node.__class__.__name__}.{event_data_class.__name__}"
    event_handler = lambda x: x
    e = GraphEventEmitter()

    mocker.patch.object(successor_node,"implemented_event_handlers",new={event_key:event_handler})
    assert event_handler == successor_node.implemented_event_handlers[ event_key ] , "mocking done incorrectly"

    EventDependency(predecessor_node,successor_node,event_data_class)

    assert event_handler in predecessor_node.get_event(event_key), "event handler should be registered to events"

    predecessor_node.notify_handlers(event_key,"hahaha")
    assert e.events[event_key].value() == "hahaha", \
        "event handling break, predecessor emit, and successor's event handler should process it"


def test_callable_register_dependency(predecessor_node,successor_node, event_data_class):
    with pytest.raises(KeyError):
        a = CallableDependency(predecessor_node,successor_node,event_data_class)


def test_callable_register_dependency_missing_handler(mocker:MockFixture, predecessor_node,
                                                      successor_node, interface_class):
    interface_key =f"{predecessor_node.__class__.__name__}.{interface_class.__name__}"

    mocker.patch.object(predecessor_node,"implemented_interfaces",new={interface_key: predecessor_node})
    assert predecessor_node == predecessor_node.implemented_interfaces[interface_key], "mocking done incorrectly"

    CallableDependency(predecessor_node,successor_node,interface_class)
    assert interface_key in successor_node.registered_interfaces.keys(), "registration failed, key not found"
    assert issubclass(successor_node.registered_interfaces[interface_key].__class__, interface_class), \
        "predecessor does not implement InterfaceClass"
    assert successor_node.registered_interfaces[interface_key].interface_func("hahaha") == "hahaha", \
        "callable handling break, successor call the function, it should be the predecessor's implementation"
