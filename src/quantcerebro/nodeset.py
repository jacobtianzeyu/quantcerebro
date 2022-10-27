"""

"""
# standard lib imports
from __future__ import annotations

from dataclasses import dataclass , field
from typing import Optional , Dict , Any , List , cast

# Local application/library specific imports.
from .node import Node
from .dependencies import Dependency , EdgeConfig
from .event import GraphEvent
from .meta import ScenarioComponent , Config

# 3rd-party imports
...


class NodeSet(ScenarioComponent):

    def __init__(self , nodeset_config: Optional[ NodeSetConfig ] = None):
        super(NodeSet , self).__init__()
        self.nodeset_config = nodeset_config
        self.children: List[ ScenarioComponent ] = list()
        self.edges = list()

    @property
    def name(self) -> str:
        return self.nodeset_config.name

    @property
    def implemented_event_handlers(self) -> Optional[ Dict[ str , Any ] ]:
        return None

    @property
    def implemented_interfaces(self) -> Optional[ Dict[ str , Any ] ]:
        return None

    @property
    def event_emitter(self) -> Optional[ Dict[ str , Any ] ]:
        return None

    @property
    def registered_events(self) -> Optional[ Dict[ str , GraphEvent ] ]:
        return None

    @property
    def registered_interfaces(self) -> Optional[ Dict[ str , Any ] ]:
        return None

    # composite method
    def is_nodeset(self) -> bool:
        return True

    # composite method
    def get_nodeset(self , name: Optional[ str ] = None) -> NodeSet:
        if (name is None) or (name == self.name):
            return self
        else:
            stack: List[ ScenarioComponent ] = list()
            stack.append(self)
            while stack:
                current_component = stack.pop()
                if current_component.is_nodeset():
                    if current_component.name == name:
                        return cast(NodeSet , current_component)
                    for c in cast(NodeSet , current_component).children:
                        stack.append(c)

            raise KeyError(f"child nodeset: '{name}' not found")

    # composite method
    def has_child_nodeset(self) -> bool:
        for c in self.children:
            if c.is_nodeset():
                return True

        return False

    def get_child_component(self , name: str) -> ScenarioComponent:
        stack: List[ ScenarioComponent ] = list()
        stack.append(self)
        while stack:
            current_component = stack.pop()
            if current_component.is_nodeset():
                if current_component.name == name:
                    return current_component
                for c in cast(NodeSet , current_component).children:
                    stack.append(c)
            else:
                if current_component.name == name:
                    return current_component

        raise KeyError(f"child component: '{name}' not found")

    # composite method
    def get_child_node(self , name: str) -> Node:
        stack: List[ ScenarioComponent ] = list()
        stack.append(self)
        while stack:
            current_component = stack.pop()
            if current_component.is_nodeset():
                for c in cast(NodeSet , current_component).children:
                    stack.append(c)
            else:
                if current_component.name == name:
                    return cast(Node , current_component)

        raise KeyError(f"child node: '{name}' not found")

    # operational
    def get_child_node_by_tag(self , tag: str) -> Node:
        "get child node by dependency tag"
        stack: List[ ScenarioComponent ] = list()
        stack.append(self)
        while stack:
            current_component = stack.pop()
            if current_component.is_nodeset():
                for c in cast(NodeSet , current_component).children:
                    stack.append(c)
            else:
                node = cast(Node , current_component)
                if node.dependency_tag == tag:
                    return node

        raise KeyError(f"child node with tag: '{tag}' not found")

    # composite method
    def add_child(self , component: ScenarioComponent):
        """attach child component, and set the component's parent to ``self`` """
        component.parent = self
        self.children.append(component)

    # composite method
    def remove_child(self , component: ScenarioComponent):
        self.children.remove(component)

    # composite method
    def add_edge(self , edge: Dependency):
        self.edges.append(edge)

    def add_event(self , node_name: str , event_name: str):
        node = self.get_child_node(node_name)
        node.add_event(node_name , event_name)

    def get_event(self , node_name: str , event_name: str) -> GraphEvent:
        node = self.get_child_node(node_name)
        return node.get_event(node_name , event_name)

    def register_interface_to_node(self , node_name: str , interface_name: str , interface):
        node = self.get_child_node(node_name)
        node.register_interface_to_node(node_name , interface_name , interface)

    def register_handler_to_event(self , node_name: str , event_name: str , handler):
        node = self.get_child_node(node_name)
        node.register_handler_to_event(node_name , event_name , handler)

    def notify_handlers(self , node_name: str , event_name: str , *msg):
        node = self.get_child_node(node_name)
        node.notify_handlers(node_name , event_name , *msg)

    def consolidate_implemented_interfaces(self):
        for c in self.children:
            c.consolidate_implemented_interfaces()

    def consolidate_implemented_handlers(self):
        for c in self.children:
            c.consolidate_implemented_handlers()


@dataclass
class NodeSetConfig(Config):
    nodeset_class: str
    components: List[ Config ] = field(default_factory=list)
    edges: List[ EdgeConfig ] = field(default_factory=list)

    @classmethod
    def from_dict(cls , input: Dict[ str , str ]):
        scenario_name = input[ "name" ]
        scenario_class = input[ "nodesetClass" ]
        scenario_config_class = input[ "nodesetConfigClass" ]
        return cls(scenario_name , scenario_config_class , scenario_class)

    def add_child_config(self , config: Config):
        config.parent = self
        self.components.append(config)

    def add_edge_config(self , edge: EdgeConfig):
        self.edges.append(edge)

    def is_nodeset_config(self):
        return True

    def get_child_component_config(self , name: str) -> Config:
        stack: List[ Config ] = list()
        stack.append(self)
        while stack:
            current_component = stack.pop()
            if current_component.is_nodeset_config():
                if current_component.name == name:
                    return current_component
                for c in cast(NodeSetConfig , current_component).components:
                    stack.append(c)
            else:
                if current_component.name == name:
                    return current_component

        raise KeyError(f"child component: '{name}' not found")

    def get_nodeset_config(self , name: str):

        if (name is None) or (name == self.name):
            return self
        else:
            stack: List[ Config ] = list()
            stack.append(self)
            while stack:
                current_component_config = stack.pop()
                if current_component_config.is_nodeset_config():
                    if current_component_config.name == name:
                        return cast(NodeSet , current_component_config)
                    for c in cast(NodeSetConfig , current_component_config).components:
                        stack.append(c)

            raise KeyError(f"child nodeset config: '{name}' not found")
