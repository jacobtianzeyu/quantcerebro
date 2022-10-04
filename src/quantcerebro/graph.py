from __future__ import annotations

import logging
from importlib import import_module
from dataclasses import dataclass , field
from typing import Set , List , Any , Dict , Optional

from .dependencies import Dependency , EventDependency , CallableDependency
from .node import Node, NodeConfig
from .utils import load_yaml , load_class


class GraphBuilder:
    """
    Graph Builder that
    - reads from config file and build a `Graph` object
    - reads from cofig and build a `Graph` object
    """
    logger = logging.getLogger(__name__)

    @classmethod
    def build_from_file(cls , file_path:str) -> Graph:
        file = load_yaml(file_path)
        config = GraphConfig.from_file(file)
        graph = Graph(config)
        return graph

    @classmethod
    def build_from_config(cls,config:GraphConfig)-> Graph:
        graph = Graph(config)
        return graph


class Graph:
    """
    Graph is a set of nodes, their dependencies are determined by edge
    """
    def __init__(self, graph_config: GraphConfig) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = graph_config
        self.name = graph_config.name
        self.nodes: Set[ Node ] = set()
        self.edges: Set[ Dependency ] = set()
        self.load_nodes()
        self.load_edges()

    def load_nodes(self):

        for nd in self.config.nodes:
            if nd.graph_class is not None:
                self.logger.info(f"loading graph {nd}")
                klass = load_class(nd.graph_class)
                node_instance = klass(nd.path)
                node_instance.name = nd.name
                self.add_node(node_instance)
            else:
                self.logger.info(f"loading nodes {nd}")
                klass = load_class(nd.node_class)
                node_config = self.config.get_node_config(nd.name)
                node_instance: Node = klass(node_config)
                self.add_node(node_instance)

    def load_edges(self):
        for e in self.config.edges:
            self.logger.info(f"loading edges {e}")

            pred_node = self.get_node_by_name(e.pred)
            succ_node = self.get_node_by_name(e.succ)
            edge_dataclass = load_class(e.edge_dataclass)

            if e.edge_type.lower() == "event":
                event_dependency = EventDependency(pred_node, succ_node, edge_dataclass)
                self.add_edge(event_dependency)

            if e.edge_type.lower() == "callable":
                callable_dependency = CallableDependency(pred_node, succ_node, edge_dataclass)
                self.add_edge(callable_dependency)

    def add_edge(self , dependency: Dependency) -> None:
        # self.config.edges.add(dependency.to_edge_section())
        self.edges.add(dependency)

    def add_node(self , node: Node) -> None:
        # self.config.nodes.add(node.to_node_section())
        self.nodes.add(node)

    def _get_node_by_name(self, name:str) -> Node:
        for n in self.nodes:
            if n.name.lower() == name.lower():
                return n
        raise Exception(f"Node Name Not Found! Available Nodes:{self.nodes}")

    def get_node_by_name(self, name:str) -> Node:
        name_list = name.split(".")
        graph = self
        for n in name_list:
            graph = graph._get_node_by_name(n)
            if hasattr(graph,"graph"):
                graph = graph.graph
        return graph

class ConfigParser:

    __slots__ = ()
    logger = logging.getLogger(__name__)
    GRAPH_NAME = 'name'
    GRAPH_NODE = 'nodes'
    GRAPH_EDGE = 'edges'
    GRAPH_NODE_CONFIGS = 'nodeConfigs'

    class Node:
        __slots__ = ()
        NAME = "name"
        NODE_CLASS = "nodeClass"
        GRAPH_CLASS = "graphClass"
        PATH = "graphPath"

    class Edge:
        __slots__ = ()
        PRED = 'pred'
        SUCC = 'succ'
        DATACLASS = 'edgeDataClass'
        TYPE = 'edgeType'
        REF = 'edgeRef'

    class NodeConfig:
        __slots__ = ()
        NAME = "name"
        DATA_CLASS = "dataClass"

    @classmethod
    def get_class_from_name(cls,class_name:str) -> Any :
        try:
            module_path,_,class_name = class_name.rpartition(".")
            mod = import_module(module_path)
            klass = getattr(mod, class_name)
            return klass
        except NameError as e:
            cls.logger.error(f"Error instantiating class{class_name} {e}")

        return None


@dataclass
class GraphConfig:
    logger = logging.getLogger(__name__)
    name: str
    nodes: List[NodeSection]
    edges: List[EdgeSection]
    node_configs: List[NodeConfig]
    graph_view: Any=field(init=False)

    @classmethod
    def from_file(cls, input:Dict[ str, Any ]) -> GraphConfig:

        name = input[ConfigParser.GRAPH_NAME]

        nodes = input[ConfigParser.GRAPH_NODE ]
        _nodes = list([NodeSection.from_file(nd) for nd in nodes]) if nodes != None else list()

        edges = input.get(ConfigParser.GRAPH_EDGE,None)
        _edges = list([EdgeSection.from_file(edge) for edge in edges]) if edges != None else list()

        node_configs = input.get(ConfigParser.GRAPH_NODE_CONFIGS, None)
        _node_configs = list()
        if node_configs is not None:
            for nc in node_configs:
                config_klass: NodeConfig = ConfigParser.get_class_from_name(nc[ConfigParser.NodeConfig.DATA_CLASS])
                temp_config = config_klass.from_file(nc)
                _node_configs.append(temp_config)
                # _node_configs = [temp_config.from_file(**nc) for nc in node_configs] if node_configs!=[None] else []

        out = cls(name, _nodes, _edges,_node_configs)
        return out

    @classmethod
    def empty_config(cls):
        out = cls("", list(), list(), list())
        return out

    # def get_node(self, name:str) -> Optional[NodeSection]:
    #     for nd in self.nodes:
    #         if nd.name == name:
    #             return nd
    #
    #     return None
    #
    # def get_edge(self,name:str) -> Optional[EdgeSection]:
    #     for edge in self.edges:
    #         if (name in edge.pred) or (name in edge.succ):
    #             return edge
    #
    #     return None

    def get_node_config(self,name:str) -> Optional[NodeConfig]:
        for nc in self.node_configs:
            if nc.name == name:
                return nc

        return None

    def view(self) -> None:
        # gv = graphviz.Digraph(self.name,filename=f'{self.name}')
        # gv.attr(compound='true')
        # gv.edges([(edge.pred,edge.succ) for edge in self.edges])
        # gv.view()
        ...


@dataclass
class NodeSection:
    """Config NodeSection"""
    name: str
    node_class: str
    graph_class: str
    path: str

    @classmethod
    def from_file(cls, input: Dict[str,Any]) -> NodeSection:
        name = input[ConfigParser.Node.NAME]
        node_class = input.get(ConfigParser.Node.NODE_CLASS, None)
        graph_class = input.get(ConfigParser.Node.GRAPH_CLASS, None)
        path = input.get(ConfigParser.Node.PATH, None)
        out = cls(name, node_class, graph_class, path)
        return out


@dataclass
class EdgeSection:
    """Config EdgeSection"""
    pred: str
    succ: str
    edge_dataclass: str
    edge_type: str

    @classmethod
    def from_file(cls,input:Dict[str, Any]) -> EdgeSection:
        pred = input[ConfigParser.Edge.PRED]
        succ = input[ConfigParser.Edge.SUCC]
        edge_dc = input[ConfigParser.Edge.DATACLASS]
        edge_type = input[ConfigParser.Edge.TYPE ]
        # edge_ref  = input[ConfigParser.Edge.REF ]
        out = cls(pred,succ,edge_dc,edge_type)
        return out

