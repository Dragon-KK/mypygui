from types import SimpleNamespace
from fastenum import Enum as FastEnum

_i = 0

class Enum(SimpleNamespace):
    @classmethod
    def contains(cls, name : str):
        return name in cls.__dict__

    @classmethod
    def str_to_enum(cls, name : str):
        return cls.__dict__.get(name)

    @staticmethod
    def auto(first = False):
        global _i
        if first:
            _i = 0
            return _i
        _i += 1
        return _i