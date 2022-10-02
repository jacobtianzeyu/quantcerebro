import pytest
from event import EventEmitter
from eventkit import Event,Op


def test_emit():
    e = EventEmitter()

    e.create_event("a")

    e.add_listener("a",lambda x,y,z: (x,y,z))

    e.emit("a", "hahaha")
    assert e.events["a"].value() == "hahaha"

    e.emit("a" , "hahha" , "haha" , "ha")
    assert e.events["a"].value() == ("hahha","haha","ha")


def test_create_event():
    e = EventEmitter()
    e.create_event("a")
    assert "a" in e.events.keys()


def test_set_event():
    e = EventEmitter()
    a = Event("a")
    e.set_event("a",a)
    assert e.events["a"] == a


def test_set_source():
    e = EventEmitter()

    e.create_event("a")
    e.create_event("b")

    e.set_source("b", "a")

    e.events[ "b" ] += lambda x: x
    e.events["a"].emit("aaa")

    assert e.events["a"].value() == "aaa"
