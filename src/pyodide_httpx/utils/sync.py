from collections.abc import AsyncIterable, Iterable

from js import Promise
from pyodide.ffi import run_sync

try:
    run_sync(Promise.resolve())
    JSPI_SUPPORTED = True
except RuntimeError:
    JSPI_SUPPORTED = False


STOP_ITERATION = object()


def syncify[T](iterable: AsyncIterable[T]) -> Iterable[T]:
    it = aiter(iterable)
    while True:
        res = run_sync(anext(it, STOP_ITERATION))
        if res is STOP_ITERATION:
            break
        else:
            yield res  # type: ignore
