from httpx import Headers, Request, Response
from httpx._client import BoundSyncStream, Client, logger
from httpx._transports.default import ResponseStream
from httpx._types import SyncByteStream
from pyodide.ffi import run_sync
from pyodide.http import pyfetch

from ._async import Timer, acquire_buffer, js_Headers, js_readable_stream_iter
from .utils.sync import syncify


def _send_single_request(self: Client, request: Request) -> Response:
    timer = Timer()
    run_sync(timer.async_start())

    if not isinstance(request.stream, SyncByteStream):
        raise RuntimeError("Attempted to send an sync request with an AsyncClient instance.")

    js_headers = js_Headers.new(request.headers.multi_items())
    with acquire_buffer(request.content) as request_body:
        res = run_sync(
            pyfetch(
                str(request.url),
                method=request.method,
                headers=js_headers,
                body=request_body,
            )
        )
    response = Response(
        status_code=res.status,
        headers=Headers(res.headers),
        stream=ResponseStream(syncify(js_readable_stream_iter(res.js_response.body))),  # type: ignore
    )

    assert isinstance(response.stream, SyncByteStream)
    response.request = request
    response.stream = BoundSyncStream(response.stream, response=response, timer=timer)
    self.cookies.extract_cookies(response)
    response.default_encoding = self._default_encoding

    logger.info(
        'HTTP Request: %s %s "%s %d %s"',
        request.method,
        request.url,
        response.http_version,
        response.status_code,
        response.reason_phrase,
    )

    return response


def patch_sync_client():
    Client._send_single_request = _send_single_request
