from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Dict , Callable , Union , Optional

from eventkit import Event , Op

from .utils import Singleton

# Event and Event Operation wthin Node
NodeEvent = Event
NodeEventOp = Op


class GraphEvent(Event):
    """
    Event Between Nodes on a graph level
    """

    def __init__(self , name: str = '' , _with_error_done_events: bool = True):
        super().__init__(name , _with_error_done_events)


class GraphEventEmitter(metaclass=Singleton):
    """
    A very basic realisation of NodeJS's event emitter to keep track of GraphEvents
    """
    events: Dict[ str , Union[ GraphEvent , Op ] ] = defaultdict(GraphEvent)

    def create_event(self , name: str):
        self.events[ name ] = GraphEvent(name)

    def add_listener(self , name: str , listener: Callable , error_callback: Optional[ Callable ] = None ,
                     done_callback: Optional[ Callable ] = None):
        self.events[ name ].connect(listener , error_callback , done_callback)

    def emit(self , name: str , *args):
        self.events[ name ].emit(*args)

    def set_source(self , name: str , source_name: str):
        source = self.events[ source_name ]
        self.events[ name ].set_source(source)
        if source.done():
            self.events[ name ].set_done()
        else:
            source.connect(self.events[ name ].emit)

    def set_event(self , name: str , event: Union[ GraphEvent , Op ]):
        self.events[ name ] = event

    def get_event(self , event_name: str) -> GraphEvent:
        return self.events[ event_name ]
