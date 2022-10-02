import pytest
from pytest_mock import MockFixture
from yaml.error import YAMLError

from src.quantcerebro.utils import Singleton, load_class, load_yaml


class Object(metaclass=Singleton):

    def __init__(self):
        self.name = "init_value"


@pytest.fixture
def mocker_open_from_valid_path(mocker: MockFixture):
    mocked_result = mocker.mock_open(read_data="{}")
    mocker.patch("src.quantcerebro.utils.open", mocked_result)


def test_singleton():
    a = Object()
    b = Object()
    a.name = "1"
    b.name = "2"
    assert a.name == b.name == "2"


def test_load_yaml_invalid_path():
    dummy_path = "invalid_path"
    with pytest.raises(FileNotFoundError, match=f"'*{dummy_path}*'"):
        out = load_yaml(dummy_path)


def test_load_yaml(mocker_open_from_valid_path):
    valid_path = "valid_path"
    out = load_yaml(valid_path)
    assert out == dict() , "Value should be mocked"


def test_load_class_invalid_attribute():
    invalid_attibute_name = "Singleton1"
    with pytest.raises(AttributeError, match=f"'*{invalid_attibute_name}*'"):
        clazz = load_class(f"utils.{invalid_attibute_name}")


def test_load_class_invalid_path():
    invalid_module_path = "utils.uti"
    with pytest.raises(ModuleNotFoundError, match=f"'*{invalid_module_path}*'"):
        clazz = load_class(f"{invalid_module_path}.Singleton")


def test_load_class(mocker:MockFixture):
    import sys
    mocker.patch("src.quantcerebro.utils.import_module", return_value=sys.modules[__name__])
    out = load_class("lll.Object")
    assert out == Object