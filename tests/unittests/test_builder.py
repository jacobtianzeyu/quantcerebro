from typing import cast

import pytest

from resources.node_a import AConfig
from resources.node_b import BConfig , B
from resources.node_d import DConfig
from src.quantcerebro import NodeSetConfig , load_class , NodeConfig
from src.quantcerebro.builder import ScenarioBuilder , ConfigBuilder
from src.quantcerebro.dependencies import EdgeConfig


class TestConfigBuilder:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.yaml_path = "/Users/zeyutian/Documents/GitHub/quantcerebro/tests/resources/scenario_ab_d.yml"

    def test_build_components(self):
        cb = ConfigBuilder(self.yaml_path)
        cb.build()
        print(cb.scenario_config)


class TestScenarioBuilder:

    @pytest.fixture(autouse=True)
    def setup(self):
        # scenario 1 AB - C
        self.nodeset_config :NodeSetConfig = NodeSetConfig("base_node","src.quantcerebro.nodeset.NodeSetConfig","src.quantcerebro.nodeset.NodeSet")
        node_a_config = AConfig("a","tests.resources.node_a.AConfig","tests.resources.node_a.A","a","")
        node_b_config = BConfig("b","tests.resources.node_b.BConfig","tests.resources.node_b.B","b","")
        node_d_config = DConfig("d" , "tests.resources.node_d.DConfig" , "tests.resources.node_d.D", "d","")
        edge_ab_config = EdgeConfig("a","b","tests.resources.node_a.InterfaceA","callable")

        child_nodeset_config = NodeSetConfig("child_nodeset","src.quantcerebro.nodeset.NodeSetConfig","tests.resources.nodeset_ab.SetOne",list())
        edge_ab_d_config = EdgeConfig("child_nodeset.b","d","tests.resources.node_b.BEvent","event")

        child_nodeset_config.add_child_config(node_a_config)
        child_nodeset_config.add_child_config(node_b_config)
        self.nodeset_config.add_child_config(child_nodeset_config)
        self.nodeset_config.add_child_config(node_d_config)

        child_nodeset_config.add_edge_config(edge_ab_config)

        self.nodeset_config.add_edge_config(edge_ab_d_config)

        # scenario 2 AB - AC - D
        self.nodeset_config2: NodeSetConfig = NodeSetConfig("base_node" , "src.quantcerebro.nodeset.NodeSetConfig" ,
                                       "src.quantcerebro.nodeset.NodeSet" , list())
        node_a1_config = AConfig("a1" , "tests.resources.node_a.AConfig" , "tests.resources.node_a.A" ,"", "")
        node_a2_config = AConfig("a2" , "tests.resources.node_a.AConfig" , "tests.resources.node_a.A" , "" , "")
        node_b_config = BConfig("b" , "tests.resources.node_b.BConfig" , "tests.resources.node_b.B" , "" , "")
        node_c_config = BConfig("c" , "tests.resources.node_c.CConfig" , "tests.resources.node_c.C" , "" , "")
        node_d_config = DConfig("d" , "tests.resources.node_d.DConfig" , "tests.resources.node_d.D" , "" , "")

        child_nodeset_config1 = NodeSetConfig("child_nodeset1" , "src.quantcerebro.nodeset.NodeSetConfig" ,
                                             "tests.resources.nodeset_ab.SetOne" , list())

        child_nodeset_config2 = NodeSetConfig("child_nodeset2" , "src.quantcerebro.nodeset.NodeSetConfig" ,
                                              "src.quantcerebro.nodeset.NodeSet" , list())

        child_nodeset_config1.add_child_config(node_a1_config)
        child_nodeset_config1.add_child_config(node_b_config)

        child_nodeset_config2.add_child_config(node_a2_config)
        child_nodeset_config2.add_child_config(node_c_config)

        self.nodeset_config2.add_child_config(child_nodeset_config1)
        self.nodeset_config2.add_child_config(child_nodeset_config2)
        self.nodeset_config2.add_child_config(node_d_config)

    def test_build_components(self):
        cb = ConfigBuilder("/Users/zeyutian/Documents/GitHub/quantcerebro/tests/resources/scenario_ab_d.yml")
        cb.build()
        nodeset_config = cb.scenario_config
        # nodeset_config = self.nodeset_config
        builder = ScenarioBuilder(nodeset_config)

        scenario = builder.build_components()
        assert scenario.name == nodeset_config.name
        for c in nodeset_config.components:
            klazz = load_class(c.config_class)
            if issubclass(klazz, NodeSetConfig):
                child_nodeset = scenario.get_nodeset(c.name)
                assert child_nodeset.name == c.name
            else:
                child_node = scenario.get_child_node(c.name)
                assert child_node.name == c.name
                assert child_node.model.return_attr() == cast(load_class(c.config_class), c).attr

    def test_build(self):
        cb = ConfigBuilder("/Users/zeyutian/Documents/GitHub/quantcerebro/tests/resources/scenario_ab_d.yml")
        cb.build()
        nodeset_config = cb.scenario_config
        # nodeset_config = self.nodeset_config
        builder = ScenarioBuilder(nodeset_config)

        scenario = builder.build()
        assert scenario.name == nodeset_config.name
        assert cast(B, scenario.get_child_node("B")).registered_interfaces["A.InterfaceA"].interface_method() == "interface_return_value"
        scenario.get_child_node("A").event_emitter.get_event("B.BEvent").emit("emitted event")
        assert scenario.get_child_node("D").event_value == "emitted event"

        # print(cast(B, scenario.get_child_node("b")).registered_interfaces["A.InterfaceA"].interface_method() )





# import pytest
# from pytest_mock import MockFixture
#
# from src.quantcerebro import load_yaml
# from src.quantcerebro.event import GraphEventEmitter
# from src.quantcerebro.node import PredecessorTemplate, SuccessorTemplate, Node, NodeConfig, NodeSetConfig, Scen
# # from src.quantcerebro._builder import NodeSetConfig, ScenarioBuilder, ConfigParser, NodeSection, EdgeSection
#
#
# class TestGraphBuilder:
#
#     @pytest.fixture(autouse=True)
#     def setup(self):
#         self.simple_graph_path = "./resources/scenario_a_b.yml"
#         self.simple_graph_config = NodeSetConfig.from_file(load_yaml(self.simple_graph_path))
#         self.nodeset_graph_path = "./resources/composite_scenaio_config.yml"
#         self.nodeset_graph_config = NodeSetConfig.from_file(load_yaml(self.nodeset_graph_path))
#
#     def test_build(self):
#         g = ScenarioBuilder.build(self.simple_graph_path)
#         for i in g.nodes:
#             assert i.name in ["A","B"]
#
#     def test_load_nodes(self):
#         g = Node(self.simple_graph_config.name)
#
#         ScenarioBuilder._load_nodes(g, self.simple_graph_config)
#
#         for i in g.nodes:
#             assert i.name in ["A","B"]
#
#         # g = Graph(self.nodeset_graph_config.name)
#         # GraphBuilder._load_nodes(g,self.nodeset_graph_config)
#         # for i in g.nodes:
#         #     assert i.name in ["Set1", "A"]
#
#     def test_load_edges(self):
#         g = Node(self.simple_graph_config.name)
#         ScenarioBuilder._load_nodes(g,self.simple_graph_config)
#         ScenarioBuilder._load_edges(g,self.simple_graph_config)
#
#         for i in g.edges:
#             assert i.pred_node.name == "A"
#             assert i.succ_node.name == "B"
#             assert i.succ_node.registered_interfaces["A.ISimpleInterface"].interface_method() == "interface_return_value"
#
#
#
#
# class TestGraph:
#     ...
#
#
# class TestConfigParser:
#     ...
#
#
# class TestGraphConfig:
#     ...
#
#
# class TestNodeSection:
#     ...
#
#
# class TestEdgeSection:
#     ...
