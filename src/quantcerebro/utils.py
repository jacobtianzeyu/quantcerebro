from importlib import import_module
from yaml import safe_load
from typing import Dict , Any , Awaitable


class Singleton(type):
    """
    - usage:
        class A(metaclass=Singleton):
            ...
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def load_yaml(file: str) -> Dict[ str , Any ]:
    """
    read yaml file into dictionary
    :param file: "yaml/file/path"
    :return: dictionary of file
    """
    try:
        with open(file , "r") as stream:
            out = safe_load(stream)
    except FileNotFoundError as exc:
        raise exc

    return out


def load_class(path: str):
    """
    load class object from class path
    :param path: "path.to.the.class"
    :return: class object
    """
    try:
        components = path.split('.')
        mod = import_module(".".join(components[ :-1 ]))
        mod = getattr(mod , components[ -1 ])
    except AttributeError as exc:
        raise exc
    except ModuleNotFoundError as exc2:
        raise exc2

    return mod