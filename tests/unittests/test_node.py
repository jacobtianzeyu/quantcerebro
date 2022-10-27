import pytest
from pytest_mock import MockFixture

from abc import ABC
from dataclasses import dataclass
from typing import Dict , Any


from src.quantcerebro.event import GraphEventEmitter
from src.quantcerebro.node import Node, NodeConfig


class TestNode:
    @pytest.fixture(autouse=True)
    def setup(self, mocker:MockFixture):
        self.node_config = NodeConfig("a","","","")
        mocker.patch("src.quantcerebro.node.Node.init_model",return_value=None)
        self.node = Node(self.node_config)

    def test_init(self):
        assert self.node.node_config == self.node_config

    def test_name(self):
        assert self.node.name == self.node_config.name

    def test_implemented_interfaces(self):
        assert self.node.implemented_interfaces is None

    def test_event_emitter(self):
        assert self.node.event_emitter == GraphEventEmitter()

    def test_registered_events(self):
        assert self.node.registered_events == GraphEventEmitter().events

    def test_registered_interfaces(self):
        assert self.node.registered_interfaces == dict()

    def test_init_model(self):
        assert self.node.model == None

    def test_is_nodeset(self):
        assert self.node.is_nodeset() == False

    def test_add_event(self):
        self.node.add_event("a","eventa")
        assert "eventa" in self.node.registered_events
        self.node.add_event("b","eventb")
        assert  "eventb" not in self.node.registered_events

    def test_get_event(self):
        self.node.add_event("a" , "eventa")
        with pytest.raises(Exception):
            self.node.get_event("b","eventa")
        with pytest.raises(KeyError):
            self.node.get_event("a","eventb")

    def test_register_handler_to_event(self):
        ...

    def test_notify_handlers(self):
        ...

    def test_register_interface_to_node(self):
        ...

    def test_consolidate_implemented_handlers(self):
        ...

    def test_consolidate_implemented_interfaces(self):
        ...


class TestNodeConfig:
    ...

#
# class TestPredecessorNode:
#
#     @pytest.fixture(autouse=True)
#     def setup(self, prednode):
#         self.prednode = prednode
#
#     def test_init(self):
#         assert self.prednode.event_emitter == GraphEventEmitter() #EventEmitter is a SingletonClass
#         assert "ITesting" in self.prednode.implemented_interfaces
#
#     def test_init_model(self):
#         ...
#
#     def test_add_event(self):
#         assert "add_event" not in self.prednode.event_emitter.events
#         self.prednode.add_event("add_event")
#         assert "add_event" in self.prednode.event_emitter.events
#
#     def test_get_event(self):
#         with pytest.raises(KeyError, match="Event Not Found"):
#             self.prednode.get_event("a")
#
#         self.prednode.add_event("a")
#         g = GraphEventEmitter()
#         assert g.events["a"] == self.prednode.get_event("a")
#
#     def test_register_handler_to_event(self):
#         event_handler = lambda x:x
#         event_name = "register_handler_to_event"
#         assert event_name not in self.prednode.event_emitter.events
#         with pytest.raises(KeyError):
#             self.prednode.register_handler_to_event(event_name, event_handler)
#
#         self.prednode.add_event(event_name)
#         assert None == self.prednode.notify_handlers(event_name,"msg")
#         self.prednode.register_handler_to_event(event_name, event_handler)
#         assert "msg" == self.prednode.get_event(event_name).value()
#
#     def test_notify_handlers(self):
#         event1_handler = lambda x: x
#         event1_name = "event1_name"
#         self.prednode.add_event(event1_name)
#         self.prednode.register_handler_to_event(event1_name , event1_handler)
#         self.prednode.notify_handlers(event1_name , "msg")
#         assert "msg" == self.prednode.get_event(event1_name).value()
#
#     def test_consolidate_implemented_interfaces(self):
#         assert self.prednode.test() == 1
#
#
# class TestSuccessorNode:
#
#     @pytest.fixture(autouse=True)
#     def setup(self, succnode):
#         self.succnode = succnode
#
#     def test_init(self):
#         assert self.succnode.registered_interfaces == dict()
#         assert self.succnode.implemented_event_handlers == dict()
#
#     def test_init_model(self):
#         ...
#
#     def test_register_interface_to_node(self, prednode):
#         self.succnode.register_interface_to_node("ITesting", prednode.implemented_interfaces["ITesting"])
#         assert self.succnode.registered_interfaces["ITesting"].test() == 1
#
#     def test_consolidate_implemented_handlers(self):
#         ...
#
#
# class TestNode:
#     @pytest.fixture(autouse=True)
#     def setup(self, fullnode):
#         self.fullnode = fullnode
#
#     def test_init(self):
#         assert isinstance(self.fullnode.config, FullNodeConfig)
#         assert isinstance(self.fullnode.model, FullNodeModel)
#         assert self.fullnode.name == "nodename"
#
#     def test_init_model(self):
#         assert self.fullnode.model.testattr == "testattr"
#
#     def test_request_config(self):
#         ...
#
#
# class TestNodeConfig:
#
#     def test_from_file(self):
#         fullnodeconfig = FullNodeConfig("nodename","","testattr")
#         assert fullnodeconfig.test == "testattr"
#         assert fullnodeconfig.name == "nodename"
#
#
# class TestNodeConfigManager:
#     ...
#
