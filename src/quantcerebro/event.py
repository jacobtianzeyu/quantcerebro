from __future__ import annotations

from typing import Dict , Callable , Any
from eventkit import Event

from utils import Singleton


class EventEmitter(metaclass=Singleton):
    """
    A very basic realisation of NodeJS's event emitter...
    """
    events: Dict[str,Event] = dict()

    def create_event(self,name:str):
        self.events[name] = Event(name)

    def add_listener(self, name:str, listener: Callable):
        self.events[name] += listener

    def emit(self, name:str, data:Any):
        self.events[name].emit(data)