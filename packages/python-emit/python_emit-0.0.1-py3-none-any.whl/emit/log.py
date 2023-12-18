import logging
from typing import Any, Callable, ParamSpec, TypeVar
import json

from emit.utils import getcallermodule
from emit.context import getcontext

T = TypeVar("T")
Q = TypeVar("Q")
P = ParamSpec("P")


def wrap(wrapper: Callable[P, Any]):
    def _wrap(wrapped: Callable[P, Q]) -> Callable[P, Q]:
        return wrapped
    return _wrap


class BaseLog:
    def __init__(self, level: int, msg: object, *args, **kwargs):
        self.level = level
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

    def __emit__(self):
        logger = logging.getLogger(getcallermodule().__name__)
        full_log = f"{self.msg}\n{json.dumps(getcontext(), indent=2, sort_keys=True, default=str)}"

        logger.log(
            self.level,
            full_log,
            *self.args,
            **self.kwargs,
        )


@wrap(logging.log)
class Log(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@wrap(logging.debug)
class Debug(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(logging.DEBUG, *args, **kwargs)


@wrap(logging.info)
class Info(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(logging.INFO, *args, **kwargs)


@wrap(logging.warn)
class Warn(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(logging.WARN, *args, **kwargs)


@wrap(logging.error)
class Error(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(logging.ERROR, *args, **kwargs)


@wrap(logging.fatal)
class Fatal(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(logging.FATAL, *args, **kwargs)


@wrap(logging.critical)
class Crit(BaseLog):
    def __init__(self, *args, **kwargs):
        super().__init__(logging.CRITICAL, *args, **kwargs)
