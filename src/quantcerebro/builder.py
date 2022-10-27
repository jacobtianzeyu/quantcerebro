""" Builder for Scenario: :class:`.NodeSet`, :class:`.Node` and Scenario Config: :class:`.NodeSetConfig`, :class:`.NodeConfig`.

There are two classes implemented: :class:`.ConfigBuilder` and :class:`.ScenarioBuilder`


Scenario Configuration:
-------------------------------

Scenario Configuration is specified in yaml format, and takes the below construct.

    .. code-block:: yaml

        ---
        name: ...
        nodesetClass: ...
        nodesetConfigClass: ...
        components:
            - name: ...
              nodeClass: ...
            - name: ...
              nodesetClass: ...
        edges:
            - pred: ...
              succ: ...
              edgeType: ...
              edgeClass: ...
        componentConfigs:
            - name: ...
              configClass: ...
              ...
            - name: ...
              nodesetPath: ...


Configuration File keywords:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``name``: scenario name,

    .. note::

        when a nodeset is a sub-scenario, the ``component.name`` defined in parent scenario will overwrite this name.

* ``nodesetClass``: scenario class path, by default, you may specify as :class:`quantcerebro.nodeset.NodeSet`

    .. note::

        when a nodeset is a sub-scenario, the ``component.nodesetClass`` defined in parent scenario will overwrite this field.

* ``nodesetConfigClass``: scenario config class path, by default, you may specify as :class:`quantcerebro.nodeset.NodeSetConfig`

* ``components``: component section, component can be a type :class:`.Node`, or type :class:`.NodeSet`

    * ``components.name``: component name

        .. note::

            * this field is required to be unique in a scenario configuration setup.
            * this field will overwrite ``name`` of a sub-scenario, as subscenario is identified by ``componentConfigs.nodesetpath``

    * ``components.nodeClass``: node as a component, and this field specifies the class of the node

    * ``components.nodesetClass``: nodeset as a component, and this field specifies the class of the nodeset

        .. note::

            this field will overwrite ``nodesetClass`` of a sub-scenario, where sub-scenario is identified by ``componentConfigs.nodesetpath``

* ``edges``: dependency section, which specifies dependencies among components

    * ``edges.pred``: predecessor component name

        .. note::

            * when component is a node, this is the node name
            * when component is a nodeset, this is [nodeset name].[node name], though only the last [node name] matters.

    * ``edges.succ``: successor component name, same as edges.succ

    * ``edges.edgeType``: dependency type: `callable` or `event`

    * ``edges.edgeClass``: data class that handles the dependency data from pred to succ.

* ``componentConfigs``:     config section for component configs that used to initialise component a component

    * ``componentConfigs.name``:    component name as reference, there must be a one-to-one mapping with component section.

    * ``componentConfigs.[...]``:   other user defined attributes when component is a node

    * ``componentConfigs.nodesetPath``:    nodeset's path when component is a pre-defined nodeset

"""

# standard lib imports
from __future__ import annotations

from typing import cast , List , Tuple , Dict , Any

# Local application/library specific imports.
from src.quantcerebro.node import NodeConfig , Config , ScenarioComponent
from src.quantcerebro.utils import load_class ,  load_yaml
from src.quantcerebro.dependencies import Dependency , EdgeConfig , EventDependency , CallableDependency
from src.quantcerebro.nodeset import NodeSetConfig , NodeSet

# 3rd-party imports
...




def build_scenario(file_path:str) -> NodeSet:
    config_builder = ConfigBuilder(file_path)
    scenario_config = config_builder.build()
    scenario_builder = ScenarioBuilder(scenario_config)
    return scenario_builder.build()


class ScenarioBuilder:
    """
    Builds a composite scenario from composite config.
    """

    def __init__(self , nodeset_config: NodeSetConfig):
        """
        :param nodeset_config: composite scenario config
        """
        self.nodeset_config = nodeset_config
        self.scenario: NodeSet = cast(NodeSet , ScenarioBuilder.init_component_with_config(self.nodeset_config))  # root
        self.current_nodeset: NodeSet = self.scenario
        self.name_stack: List[ str ] = list()

    def build(self) -> NodeSet:
        """
        build components, then build dependencies , finally returns the built scenario
        """
        self.build_components()

        self.build_edges()

        return self.scenario

    # component
    def build_components(self) -> NodeSet:
        """
        instantiate child component level by level from the top. Stack keeps track of a nodeset by name and it's child
        configs, while stack is not empty, add each element from stack to it's parent nodeset. After components are
        instantiated, consolidate all implemented interfaces and implemented handlers. These two functions puts
        implemented interface (event handlers) into a dictionary, so it can be referenced.

        .. note::

            component name should be unique in a scenario

        :return: the scenario with all child component instantiated, but no dependencies are registered.
        """
        # stack to keep track of the leaf to construct - (name, config), it keeps track of the parent the leaf has
        stack: List[ Tuple[ str , Config ] ] = [ (self.nodeset_config.name , self.nodeset_config) ]

        # while stack is not empty
        while stack:

            parent_nodeset_name , config = stack.pop()
            component = ScenarioBuilder.init_component_with_config(config)

            self.name_check(str(component.name))

            # get current nodeset
            if parent_nodeset_name != self.current_nodeset.name:
                self.current_nodeset = self.scenario.get_nodeset(parent_nodeset_name)

            # add component to current_nodeset

            # when component is a nodeset
            if isinstance(config , NodeSetConfig):
                # if component is not "scenario" itself, add component to current_nodeset, else do nothing
                if component.name != self.scenario.name:
                    self.add_component(component)
                    parent_nodeset_name = component.name

                # push (parent_nodeset_name, config) to stack
                for n in config.components:
                    stack.append((parent_nodeset_name , n))
            # when component is a node
            else:
                self.add_component(component)

        self.scenario.consolidate_implemented_interfaces()
        self.scenario.consolidate_implemented_handlers()
        return self.scenario

    def add_component(self , component: ScenarioComponent , switch_to: bool = True):
        """ add a scenario component to current nodeset level, when switch_to is true and current component is a nodeset, switch to this nodeset branch
        :param component: scenario component
        :param switch_to: whether to switch to the added nodeset or not
        """
        self.current_nodeset.add_child(component)
        if switch_to:
            if isinstance(component , NodeSet):
                self.current_nodeset = cast(NodeSet , component)

    # edge
    def build_edges(self) -> NodeSet:
        """
        register configured dependnecies level by level. Stack keeps track of a nodeset by name and it's child  configs,
        edge_stack keep tracks a nodeset, and it's child config dependencies. After edge_stack is fully populated,
        iterate through and register dependencies one by one
        :return: the scenario with all dependencies built
        """
        stack: List[ Tuple[ str , Config ] ] = [ (self.nodeset_config.name , self.nodeset_config) ]
        edge_stack: List[ Tuple[ str , EdgeConfig ] ] = [ ]
        while stack:
            parent_nodeset_name , config = stack.pop()
            if parent_nodeset_name != self.current_nodeset.name:
                self.current_nodeset = self.scenario.get_nodeset(parent_nodeset_name)

            if isinstance(config , NodeSetConfig):
                if self.scenario.name != config.name:
                    parent_nodeset_name = config.name

                for n in config.components:
                    stack.append((parent_nodeset_name , n))

                for e in config.edges:
                    edge_stack.append((parent_nodeset_name , e))

        while edge_stack:
            parent_nodeset_name , e = edge_stack.pop()

            if parent_nodeset_name != self.current_nodeset.name:
                self.set_current_nodeset(self.scenario.get_nodeset(parent_nodeset_name))

            pred_node = self.scenario.get_child_node_by_tag(e.pred.split(".")[ -1 ])
            succ_node = self.scenario.get_child_node_by_tag(e.succ.split(".")[ -1 ])
            edge_dataclass = load_class(e.edge_dataclass)

            if e.edge_type.lower() == "event":
                event_dependency = EventDependency(pred_node , succ_node , edge_dataclass)
                self.add_edge(event_dependency)

            if e.edge_type.lower() == "callable":
                callable_dependency = CallableDependency(pred_node , succ_node , edge_dataclass)
                self.add_edge(callable_dependency)

        return self.scenario

    def add_edge(self , edge: Dependency):
        """add a dependency to a nodeset"""
        self.scenario.consolidate_implemented_interfaces()
        self.scenario.consolidate_implemented_handlers()
        self.current_nodeset.add_edge(edge)

    # auxiliaries
    def set_current_nodeset(self , nodeset: NodeSet):
        """set current nodeset pointer to the input"""
        self.current_nodeset = nodeset

    @staticmethod
    def init_component_with_config(config: Config) -> ScenarioComponent:
        """
        takes in a config of scenario component, and build it
        :param config: either type :class:`.NodeConfig` or type :class:`.NodeSetConfig`
        :return: child component of scenario
        """
        # load configclass
        # init class with config
        if isinstance(config , NodeSetConfig):
            config = cast(NodeSetConfig , config)
            klazz = load_class(config.nodeset_class)
        else:
            config = cast(NodeConfig , config)
            klazz = load_class(config.node_class)

        return klazz(config)

    def name_check(self , name: str) -> None:
        """check if name is already used"""
        if name in self.name_stack:
            raise Exception(
                f"name '{name}' is already used in {cast(NodeSet , self.scenario.get_child_component(name).parent).name}")
        else:
            self.name_stack.append(name)

    # def build2(self) -> NodeSet:
    #     # not used
    #     nodeset_klazz = load_class(self.nodeset_config.nodeset_class)
    #     scenario = cast(NodeSet, nodeset_klazz(self.nodeset_config))
    #
    #     stack:List[Config] = list()
    #     stack.append(self.nodeset_config)
    #     while stack:
    #         current_config = stack.pop()
    #         if isinstance(current_config, NodeSetConfig):
    #             for n in current_config.components:
    #                 stack.append(n)
    #         else:
    #             current_config = cast(NodeConfig, current_config)
    #             node_klazz = load_class(current_config.node_class)
    #             node = node_klazz(current_config)
    #             scenario.add_child(node)
    #             print(node.name)
    #
    #     return scenario


class ConfigBuilder:
    """
    ConfigBuilder takes in a yaml file, and returns a composite configuration :class:`.NodeSetConfig`

    :param file_path: configuration file location
    """
    NODESET_NAME = "name"
    NODESET_CONFIG_CLASS = "nodesetConfigClass"
    NODESET_CLASS = "nodesetClass"

    COMPONENTS = "components"
    COMPONENT_NAME = "name"
    NODE_CLASS = "nodeClass"

    EDGES = "edges"
    EDGE_PRED = "pred"
    EDGE_SUCC = "succ"
    EDGE_TYPE = "edgeType"
    EDGE_CLASS = "edgeClass"

    COMPONENT_CONFIGS = "componentConfigs"
    COMPONENT_CONFIG_NAME = "name"
    NODE_CONFIG_CLASS = "configClass"
    NODESET_PATH = "nodesetPath"


    def __init__(self , file_path: str):
        self.config_dict = self.process_dict(load_yaml(file_path))
        self.scenario_config: NodeSetConfig = cast(NodeSetConfig ,
                                                   ConfigBuilder.init_component_config_with_dict(self.config_dict))
        self.current_nodeset_config: NodeSetConfig = self.scenario_config
        self.name_stack: List[ str ] = list()

    def build(self) -> NodeSetConfig:
        """
        :return: NodeSetConfig
        """
        self.build_components()
        self.build_edges()
        return self.scenario_config

    def build_components(self):
        stack: List[ Tuple[ str , Dict ] ] = [ (self.config_dict[ "name" ] , self.config_dict) ]
        while stack:
            parent_nodeset_name , config_dict = stack.pop()
            component_config = ConfigBuilder.init_component_config_with_dict(config_dict)

            self.name_check(component_config.name)

            if parent_nodeset_name != self.current_nodeset_config.name:
                self.current_nodeset_config = self.scenario_config.get_nodeset_config(parent_nodeset_name)

            if self.NODESET_CONFIG_CLASS in config_dict:
                if component_config.name != self.scenario_config.name:
                    self.add_component_config(component_config)
                    parent_nodeset_name = component_config.name

                for n in config_dict[ self.COMPONENTS ]:
                    stack.append((parent_nodeset_name , n))
            else:
                self.add_component_config(component_config)

    def build_edges(self):
        stack: List[ Tuple[ str , Dict ] ] = [ (self.config_dict[ self.NODESET_NAME ] , self.config_dict) ]
        edge_stack: List[ Tuple[ str , Dict ] ] = [ ]
        while stack:
            parent_nodeset_name , config_dict = stack.pop()
            if parent_nodeset_name != self.current_nodeset_config.name:
                self.current_nodeset_config = self.scenario_config.get_nodeset_config(parent_nodeset_name)

            if self.NODESET_CONFIG_CLASS in config_dict:
                if self.scenario_config.name != config_dict[ self.NODESET_NAME ]:
                    parent_nodeset_name = config_dict[self.NODESET_NAME ]

                for n in config_dict[ self.COMPONENTS ]:
                    stack.append((parent_nodeset_name , n))

                for e in config_dict[ self.EDGES ]:
                    edge_stack.append((parent_nodeset_name , e))

        while edge_stack:
            parent_nodeset_name , e = edge_stack.pop()

            if parent_nodeset_name != self.current_nodeset_config.name:
                self.set_current_nodeset_config(self.scenario_config.get_nodeset_config(parent_nodeset_name))

            ec = EdgeConfig(e[ self.EDGE_PRED ] , e[ self.EDGE_SUCC ] , e[ self.EDGE_CLASS ] , e[ self.EDGE_TYPE ])
            self.add_edge_config(ec)

        return self.scenario_config

    def add_edge_config(self , edge: EdgeConfig):
        self.current_nodeset_config.add_edge_config(edge)

    # auxiliary function
    def process_dict(self , config_dict: Dict[ str , Any ]):
        """
        the instantiated dictionary from yaml file is not in composite format, so this preprocessing step assembles it
        into a correct format
        :param config_dict: the raw format of yaml dictionary
        :return: returns a composite patterned dictionary
        """
        component_configs: List[ Dict[ str , Any ] ] = config_dict.pop(self.COMPONENT_CONFIGS) #component config section
        components: List[ Dict[ str , Any ] ] = config_dict.pop(self.COMPONENTS) # component section
        for n in components:
            for nc in component_configs:
                if n[ self.COMPONENT_NAME] == nc[ self.COMPONENT_CONFIG_NAME ]:
                    # when component is a node
                    if self.NODE_CLASS in n.keys():
                        nc[ self.NODE_CLASS ] = n[ self.NODE_CLASS ]

                    # when component is a nodeset
                    if self.NODESET_CLASS in n.keys():
                        # load nodeset details
                        new_nc = load_yaml(nc[ self.NODESET_PATH ])
                        try:
                            new_nc = self.process_dict(new_nc)
                        except KeyError as exc:
                            raise KeyError(f"nodeset {new_nc[ 'name' ]} has format issue")
                        nc.clear()

                        # update nc from new_nc
                        for key in new_nc:
                            nc[ key ] = new_nc[ key ]
                        # align name -> makesure the user defined name is used in the scenario
                        nc[ self.COMPONENT_NAME ] = n[ self.COMPONENT_NAME ]
                        nc[ self.NODESET_CLASS ] = n[ self.NODESET_CLASS ]

        # assign updated component_config to config_dict
        config_dict[ self.COMPONENTS ] = component_configs
        return config_dict

    def set_current_nodeset_config(self , nodeset_config: NodeSetConfig):
        self.current_nodeset_config = nodeset_config

    def add_component_config(self , component_config: Config , switch_to: bool = True):
        self.current_nodeset_config.add_child_config(component_config)
        if switch_to:
            if isinstance(component_config , NodeSetConfig):
                self.current_nodeset_config = component_config

    @staticmethod
    def init_component_config_with_dict(config_dict: Dict):
        if ConfigBuilder.NODESET_CONFIG_CLASS in config_dict:
            klazz: NodeSetConfig = load_class(config_dict[ ConfigBuilder.NODESET_CONFIG_CLASS ])
            return klazz.from_dict(config_dict)
        if ConfigBuilder.NODE_CONFIG_CLASS in config_dict:
            klazz: NodeConfig = load_class(config_dict[ ConfigBuilder.NODE_CONFIG_CLASS  ])
            return klazz.from_dict(config_dict)

        raise KeyError(f"input key does not have nodesetConfig or nodeConfig...{config_dict}")

    def name_check(self , name: str):
        if name in self.name_stack:
            raise Exception(
                f"name '{name}' is already used in {cast(NodeSet , self.scenario_config.get_child_component_config(name).parent).name}")
        else:
            self.name_stack.append(name)


