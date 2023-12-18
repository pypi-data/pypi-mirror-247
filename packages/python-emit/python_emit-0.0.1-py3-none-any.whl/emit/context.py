import inspect
from threading import Lock
from typing import Any, Dict
from emit.constants import CONTEXT_KEY, LOCAL_CONTEXT_KEY
from emit.utils import getcallerframe


def getcontext():
    """Generate the context from the current stack frame."""
    caller_frame = getcallerframe()
    context = GloblContext.get().copy()

    if LOCAL_CONTEXT_KEY in caller_frame.f_locals:
        context.update(caller_frame.f_locals[LOCAL_CONTEXT_KEY])

    for frame in inspect.getouterframes(caller_frame):
        if CONTEXT_KEY in frame.frame.f_locals:
            context.update(frame.frame.f_locals[CONTEXT_KEY])

    return context


class Context:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def __emit__(self):
        caller_frame = getcallerframe()

        if CONTEXT_KEY not in caller_frame.f_locals:
            caller_frame.f_locals[CONTEXT_KEY] = {}

        caller_frame.f_locals[CONTEXT_KEY].update(self.kwargs)


class LocalContext:
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs

    def __emit__(self):
        caller_frame = getcallerframe()
        if LOCAL_CONTEXT_KEY not in caller_frame.f_locals:
            caller_frame.f_locals[LOCAL_CONTEXT_KEY] = {}

        caller_frame.f_locals[LOCAL_CONTEXT_KEY].update(self.kwargs)


_global_context: Dict[str, Any] = {}
_global_context_lock = Lock()


class GloblContext:
    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    def __emit__(self):
        with _global_context_lock:
            _global_context.update(self.kwargs)

    @classmethod
    def get(cls):
        return _global_context
