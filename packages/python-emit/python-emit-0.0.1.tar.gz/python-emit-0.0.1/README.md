# Emit

A Python library for understated tracing and structured logging.

## TL;DR

```python
# This is the big idea. Now let's use it.
def emit(obj):
    return obj.__emit__()
```

## Logging

```python
from emit import emit, Info, Warning

def frobulate_the_quartzle():
    # This works like you expect, no more logger = logging.getLogger(__name__).
    # just emit and the log will originate from the right place.
    emit(Info("Frobulating the quartzle"))

    if not Quartzle.is_polarized():
        emit(Warning("Quartzle isn't polarized, results may be different than expected."))
```

## Structured Logging

```python
from emit import emit, Context

def push_noins():
    emit(Info("Noins updated."))

def shuffle_lorpizoids():
    emit(Context(current_user="Harry Styles"))

    # The log emitted from this code will include the current_user context.
    push_noins()
```

## Say No To Passing Around Loggers Just To Bind Values

```python
# In `structlog`
log = log.bind(key=value)

# In `emit`
emit(Context(key=value))
```
