from abc import ABC
from typing import Dict , Any

import pytest
from pytest_mock import MockFixture

from src.quantcerebro.event import GraphEventEmitter
from src.quantcerebro.node import PredecessorNode, SuccessorNode, Node, NodeConfig, IConfigRetriever, NodeConfigManager


@pytest.fixture(scope="class")
def prednode():
    class ITesting(ABC):
        def test(self):
            raise NotImplementedError

    class PD(PredecessorNode, ITesting):
        def init_model(self , config: NodeConfig):
            pass

        def _consolidate_implemented_interfaces(self):
            out = dict()
            out[ITesting.__name__] = self
            return out

        def test(self):
            return 1

    return PD()


@pytest.fixture(scope="class")
def succnode():

    class SuccNode(SuccessorNode):
        def _consolidate_implemented_handlers(self) -> Dict[ str , Any ]:
            pass

        def init_model(self , config: NodeConfig):
            pass

        def request(self , name: str):
            return 1

    return SuccNode()


@pytest.fixture(scope="class")
def fullnode():

    class FullNode(Node):
        def _consolidate_implemented_handlers(self) -> Dict[ str , Any ]:
            pass

        def _consolidate_implemented_interfaces(self) -> Dict[str,Any]:
            return super()._consolidate_implemented_interfaces()

        def init_model(self , config: NodeConfig):
            pass

        def request(self,name:str):
            return 1
    nd = NodeConfig("")
    return FullNode(nd)


class TestPredecessorNode:

    @pytest.fixture(autouse=True)
    def setup(self, prednode):
        self.prednode = prednode

    def test_direct_init(self):
        with pytest.raises(TypeError,match=r"abstract method"):
            PredecessorNode()

    def test_init(self):
        assert self.prednode.event_emitter == GraphEventEmitter() #EventEmitter is a SingletonClass
        assert "ITesting" in self.prednode.implemented_interfaces

    def test_init_model(self):
        ...

    def test_add_event(self):
        assert "add_event" not in self.prednode.event_emitter.events
        self.prednode.add_event("add_event")
        assert "add_event" in self.prednode.event_emitter.events

    def test_get_event(self):
        with pytest.raises(KeyError, match="Event Not Found"):
            self.prednode.get_event("a")

        self.prednode.add_event("a")
        g = GraphEventEmitter()
        assert g.events["a"] == self.prednode.get_event("a")

    def test_register_handler_to_event(self):
        event_handler = lambda x:x
        event_name = "register_handler_to_event"
        assert event_name not in self.prednode.event_emitter.events
        with pytest.raises(KeyError):
            self.prednode.register_handler_to_event(event_name, event_handler)

        self.prednode.add_event(event_name)
        assert None == self.prednode.notify_handlers(event_name,"msg")
        self.prednode.register_handler_to_event(event_name, event_handler)
        assert "msg" == self.prednode.get_event(event_name).value()

    def test_notify_handlers(self):
        event1_handler = lambda x: x
        event1_name = "event1_name"
        self.prednode.add_event(event1_name)
        self.prednode.register_handler_to_event(event1_name , event1_handler)
        self.prednode.notify_handlers(event1_name , "msg")
        assert "msg" == self.prednode.get_event(event1_name).value()

    def test_consolidate_implemented_interfaces(self):
        assert self.prednode.test() == 1


class TestSuccessorNode:
    @pytest.fixture(autouse=True)
    def setup(self, succnode):
        self.succnode = succnode


class TestNode:
    @pytest.fixture(autouse=True)
    def setup(self, fullnode):
        self.fullnode = fullnode


class TestNodeConfig:
    ...


class TestNodeConfigManager:
    ...

