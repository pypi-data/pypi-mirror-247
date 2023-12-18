import inspect

import emit


def getcallerframe():
    for frame in inspect.stack():
        mod = inspect.getmodule(frame[0])
        if mod and mod == inspect.getmodule(emit):
            if frame.frame.f_code.co_name == "emit":
                emit_frame = frame.frame
                assert emit_frame.f_back is not None
                return emit_frame.f_back

    raise RuntimeError("Couldn't find caller frame")


def getcallermodule():
    caller_frame = getcallerframe()
    mod = inspect.getmodule(caller_frame)
    assert mod is not None
    return mod
