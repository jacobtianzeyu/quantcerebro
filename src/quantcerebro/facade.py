from dependencies import Dependency
from graph import GraphBuilder , GraphConfig , Node


class AppFacade:
    def __init__(self, config_path: str=None):
        if (config_path is None) or (config_path == ""):
            config = GraphConfig.empty_config()
            self.graph = GraphBuilder.build_from_config(config)
        else:
            self.graph = GraphBuilder.build_from_file(config_path)

    def add_node(self, node: Node):
        self.graph.add_node(node)

    def add_edge(self, dependency: Dependency):
        self.graph.add_edge(dependency)

