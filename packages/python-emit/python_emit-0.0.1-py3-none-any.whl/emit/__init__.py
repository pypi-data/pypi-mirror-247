from typing import TypeVar, Protocol
from pkg_resources import parse_version

__version__ = parse_version("0.0.1")

class Emit(Protocol):
    def __emit__(self):
        pass


T = TypeVar("T", bound=Emit)


def emit(obj: T) -> T | None:
    obj.__emit__()


__all__ = ["Emit", "emit"]
