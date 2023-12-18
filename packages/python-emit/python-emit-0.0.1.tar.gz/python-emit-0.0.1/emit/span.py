import inspect
from emit import emit
from emit.constants import CONTEXT_KEY, EMIT_SPAN_KEY, LOCAL_CONTEXT_KEY
from emit.log import Debug
from emit.utils import getcallerframe


def getspans():
    caller_frame = getcallerframe()
    spans = []

    for frame in inspect.getouterframes(caller_frame):
        frame_local_context = (
            frame.frame.f_locals.get(CONTEXT_KEY, {}) |
            frame.frame.f_locals.get(LOCAL_CONTEXT_KEY, {})
        )

        if EMIT_SPAN_KEY in frame_local_context:
            spans.insert(0, frame_local_context[EMIT_SPAN_KEY])

    return spans


class Span:
    def __init__(self, span_id: str):
        self.span_id = span_id

    def __emit__(self):
        caller_frame = getcallerframe()
        if CONTEXT_KEY not in caller_frame.f_locals:
            caller_frame.f_locals[CONTEXT_KEY] = {}

        caller_frame.f_locals[CONTEXT_KEY][EMIT_SPAN_KEY] = self.span_id

        print(getspans())

def spanspan():
    emit(Debug("Hello"))

spanspan()
