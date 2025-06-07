"""Minimal typing backport for Python 3.2."""

try:
    from typing import *  # type: ignore
except Exception:  # pragma: no cover - old Python
    # Bare bones fallbacks so type hints can be imported.
    Any = object

    def cast(tp, obj):
        return obj

    class _Alias:
        def __init__(self, name):
            self.__name__ = name

        def __getitem__(self, item):
            return self

    List = _Alias("List")
    Dict = _Alias("Dict")
    Tuple = _Alias("Tuple")
    Set = _Alias("Set")
    Optional = _Alias("Optional")
    Union = _Alias("Union")
    Callable = _Alias("Callable")
    Type = _Alias("Type")

    class NamedTuple(tuple):
        pass
