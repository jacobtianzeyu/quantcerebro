from importlib import import_module
from yaml import safe_load, YAMLError
from typing import Dict , Any , Awaitable


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def load_yaml(file: str) -> Dict[ str , Any ]:
    try:
        with open(file , "r") as stream:
            out = safe_load(stream)
    except YAMLError as exc:
        raise exc

    return out


def load_class(path: str):
    components = path.split('.')
    mod = import_module(".".join(components[ :-1 ]))
    mod = getattr(mod , components[ -1 ])
    return mod