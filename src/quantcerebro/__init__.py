"""
quantcerebro
============

QuantCerebro is a Python package for building event driven programs. It provides a simple and configurable framework to
define Callable (Interface) dependency and Event dependency.

See docs for complete documentation.
"""
__version__ = '0.1.0'

from .node import Node, NodeConfig
from .graph import Graph, GraphBuilder, ConfigParser
from .facade import AppFacade
from .utils import load_yaml, load_class
from .event import NodeEvent, NodeEventOp