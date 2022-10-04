import pytest
from src.quantcerebro.event import GraphEventEmitter, GraphEvent


def test_emit():
    e = GraphEventEmitter()

    e.create_event("a")

    e.add_listener("a",lambda x,y,z: (x,y,z))

    e.emit("a", "msg")
    assert e.events["a"].value() == "msg"

    e.emit("a" , "msg1" , "msg2" , "msg3")
    assert e.events["a"].value() == ("msg1","msg2","msg3")


def test_create_event():
    e = GraphEventEmitter()
    e.create_event("a")
    assert "a" in e.events.keys()


def test_set_event():
    e = GraphEventEmitter()
    a = GraphEvent("a")
    e.set_event("a",a)
    assert e.events["a"] == a


def test_set_source():
    e = GraphEventEmitter()

    e.create_event("a")
    e.create_event("b")

    e.set_source("b", "a")

    e.events[ "b" ] += lambda x: x
    e.events["a"].emit("msg")

    assert e.events["a"].value() == "msg"
