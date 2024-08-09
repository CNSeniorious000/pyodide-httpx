from typing import Awaitable, Callable

from pyodide.ffi import JsProxy

class Promise:
    resolve: Callable[..., Awaitable[JsProxy]]

class Headers:
    new: Callable[..., Headers]
