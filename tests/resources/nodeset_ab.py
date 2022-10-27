from dataclasses import dataclass
from typing import Optional , TypedDict , cast

from resources.node_a import AConfig , A , InterfaceA
from resources.node_b import BConfig , B
from src.quantcerebro.nodeset import NodeSet , NodeSetConfig


class SetOne(NodeSet):
    def __init__(self, nodeset_config: Optional[NodeSetConfig]=None):
        super().__init__(nodeset_config)


if __name__ == "__main__":
    # nodeset_config = NodeSetConfig()
    #
    # node_a_section = NodeSection("A","tests.resources.node_a.AConfig")
    # node_b_section = NodeSection("B","tests.resources.node_b.BConfig")
    # edge_ab_section = EdgeSection("A" , "B" , "tests.resources.node_a.InterfaceA" , "callable")
    # node_a_config_section = ConfigSection("A","tests.resources.node_a.AConfig", {"attr":"attrA"},None)
    # node_b_config_section = ConfigSection("B","tests.resources.node_a.BConfig", {"attr":"attrB"},None)
    #
    # nodeset_config.nodes.append(node_a_section)
    # nodeset_config.nodes.append(node_b_section)
    # nodeset_config.edges.append(edge_ab_section)
    # nodeset_config.node_configs.append(node_a_config_section)
    # nodeset_config.node_configs.append(node_b_config_section)
    #
    # SetOne(nodeset_config)
    #
    a=SetOne()
    aconfig = AConfig("A", "Aattr")
    node_a = A(aconfig)
    node_a.consolidate_implemented_interfaces()

    bconfig = BConfig("B", "Battr")
    node_b = B(bconfig)

    a.add_child(node_a)
    a.add_child(node_b)
    node_b.register_interface_to_node(node_b.name , "InterfaceA" , node_a.implemented_interfaces[ "InterfaceA" ])

    # print(cast(InterfaceA,a.get_child_node("B").registered_interfaces["InterfaceA"]).interface_method())

