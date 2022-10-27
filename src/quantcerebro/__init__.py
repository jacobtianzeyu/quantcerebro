"""
quantcerebro
#############

QuantCerebro is a Python package the provides configurable framework to describe relationships among business logics.
The common relationship among business logic can be a. event; b. callable (interface).

See docs for complete documentation.
"""
__version__ = '0.1.0'
__docformat__ = 'reStructuredText'

from .builder import ScenarioBuilder , ConfigBuilder
from .meta import PredecessorTemplate , SuccessorTemplate , ScenarioComponent , Config
from .nodeset import NodeSet , NodeSetConfig
from .node import Node , NodeConfig
from .dependencies import EdgeConfig , Dependency , EventDependency , CallableDependency
from .event import NodeEvent , NodeEventOp , GraphEvent , GraphEventEmitter
from .utils import load_yaml , load_class
