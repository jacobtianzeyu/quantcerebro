from __future__ import annotations

from typing import Dict , Callable , Any, Union
from eventkit import Event, Op

from utils import Singleton


class EventEmitter(metaclass=Singleton):
    """
    A very basic realisation of NodeJS's event emitter...
    """
    events: Dict[str, Union[Event, Op]] = dict()

    def create_event(self,name:str):
        self.events[name] = Event(name)

    def add_listener(self, name:str, listener: Callable):
        self.events[name].connect(listener)

    def emit(self, name:str, *args):
        self.events[name].emit(*args)

    def set_source(self,name:str, source_name:str):
        source = self.events[source_name]
        self.events[name].set_source(source)
        if source.done():
            self.events[name].set_done()
        else:
            source.connect(self.events[name].emit)

    def set_event(self, name:str, event:Union[Event,Op]):
        self.events[name] = event



