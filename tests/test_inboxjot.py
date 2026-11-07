import asyncio
import re
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import httpx
import pytest
from helpers import MockApi, api_error, json_reply

from inboxjot import (
    AsyncInboxjot,
    Inboxjot,
    InboxjotConnectionError,
    InboxjotError,
    __version__,
)


def test_reads_the_api_key_from_inboxjot_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INBOXJOT_API_KEY", "ibx_env")
    api = MockApi(json_reply({}))
    http_client = httpx.Client(transport=httpx.MockTransport(api.handle))

    Inboxjot(http_client=http_client).emails.get("em_1")

    request = api.requests[0]
    assert request.headers["Authorization"] == "Bearer ibx_env"
    assert str(request.url) == "https://api.inboxjot.com/v1/emails/em_1"


def test_raises_without_an_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("INBOXJOT_API_KEY", raising=False)

    with pytest.raises(ValueError, match="Missing API key"):
        Inboxjot()
    with pytest.raises(ValueError, match="Missing API key"):
        AsyncInboxjot()


def test_sends_the_timeout_for_each_request() -> None:
    api = MockApi(json_reply({}), json_reply({}))
    inboxjot = api.client()

    inboxjot.emails.get("em_1")
    inboxjot.emails.get("em_1", timeout=5)

    assert api.requests[0].extensions["timeout"]["read"] == 60.0
    assert api.requests[1].extensions["timeout"]["read"] == 5


def test_maps_the_error_body_to_inboxjot_error() -> None:
    body = {
        "name": "validation_error",
        "status": 400,
        "message": "Invalid address",
        "errors": [{"message": "Invalid address", "location": "to"}],
        "request_id": "req_9",
    }
    api = MockApi(json_reply(body, 400))

    with pytest.raises(InboxjotError) as info:
        api.client().emails.send({"to": "x"})

    error = info.value
    assert error.name == "validation_error"
    assert error.status == 400
    assert error.message == "Invalid address"
    assert str(error) == "Invalid address"
    assert error.errors == body["errors"]
    assert error.request_id == "req_9"
    assert error.headers["content-type"] == "application/json"


def test_maps_a_body_that_is_not_json() -> None:
    reply = httpx.Response(502, text="Bad Gateway", headers={"request-id": "req_2"})
    api = MockApi(reply)

    with pytest.raises(InboxjotError) as info:
        api.client(max_retries=0).emails.get("em_1")

    error = info.value
    assert error.name == "unknown_error"
    assert error.status == 502
    assert error.message == "Bad Gateway"
    assert error.request_id == "req_2"


def test_does_not_retry_client_errors() -> None:
    api = MockApi(api_error(404, "not_found"))

    with pytest.raises(InboxjotError, match="not_found message"):
        api.client().emails.get("em_1")

    assert len(api.requests) == 1


def test_retries_a_409_concurrent_request_after_retry_after_with_the_same_key(
    sleeps: list[float],
) -> None:
    api = MockApi(
        api_error(409, "concurrent_idempotent_requests", {"Retry-After": "1"}),
        json_reply({"id": "em_1"}, 202),
    )

    result = api.client().emails.send({"to": "a@acme.dev"}, idempotency_key="k")

    assert result == {"id": "em_1"}
    assert sleeps == [1]
    assert api.requests[1].headers["Idempotency-Key"] == "k"


def test_retries_429_even_without_a_key(sleeps: list[float]) -> None:
    api = MockApi(
        api_error(429, "rate_limit_exceeded", {"Retry-After": "2"}),
        json_reply({"id": "em_1"}, 202),
    )

    result = api.client().emails.send({"to": "a@acme.dev"})

    assert result == {"id": "em_1"}
    assert sleeps == [2]
    assert len(api.requests) == 2


def test_retries_5xx_and_network_errors_on_reads(sleeps: list[float]) -> None:
    api = MockApi(
        api_error(500, "unknown_error"),
        httpx.ConnectError("connection refused"),
        json_reply({"id": "em_1"}),
    )

    result = api.client().emails.get("em_1")

    assert result == {"id": "em_1"}
    assert len(api.requests) == 3
    assert 0.375 <= sleeps[0] <= 0.5
    assert 0.75 <= sleeps[1] <= 1.0


def test_does_not_retry_5xx_or_network_errors_on_writes_without_a_key() -> None:
    server = MockApi(api_error(500, "unknown_error"))

    with pytest.raises(InboxjotError) as info:
        server.client().emails.send({"to": "a@acme.dev"})

    assert info.value.status == 500
    assert len(server.requests) == 1

    network = MockApi(httpx.ConnectError("connection refused"))

    with pytest.raises(InboxjotConnectionError, match="Connection error"):
        network.client().events.send({"name": "a", "email": "a@acme.dev"})

    assert len(network.requests) == 1


def test_retries_writes_that_carry_a_key() -> None:
    api = MockApi(
        httpx.ConnectError("connection refused"),
        api_error(503, "unknown_error"),
        json_reply({"id": "em_1"}),
    )

    result = api.client().emails.cancel("em_1", idempotency_key="k")

    assert result == {"id": "em_1"}
    assert len(api.requests) == 3


def test_stops_after_max_retries() -> None:
    api = MockApi(*[api_error(500, "unknown_error") for _ in range(3)])

    with pytest.raises(InboxjotError):
        api.client(max_retries=1).emails.get("em_1")

    assert len(api.requests) == 2


def test_per_request_max_retries_overrides_the_client() -> None:
    api = MockApi(*[api_error(500, "unknown_error") for _ in range(3)])

    with pytest.raises(InboxjotError):
        api.client(max_retries=0).emails.get("em_1", max_retries=2)

    assert len(api.requests) == 3


def test_times_out_a_slow_request() -> None:
    api = MockApi(httpx.ReadTimeout("timed out"))
    http_client = httpx.Client(transport=httpx.MockTransport(api.handle))
    inboxjot = Inboxjot(api_key="ibx_test", timeout=0.1, max_retries=0, http_client=http_client)

    with pytest.raises(InboxjotConnectionError, match=r"Request timed out after 0.1s") as info:
        inboxjot.emails.get("em_1")

    assert isinstance(info.value.__cause__, httpx.ReadTimeout)


def test_async_client_retries_and_maps_errors(sleeps: list[float]) -> None:
    api = MockApi(
        api_error(429, "rate_limit_exceeded", {"Retry-After": "1"}),
        httpx.ConnectError("connection refused"),
        api_error(404, "not_found"),
    )

    async def run() -> None:
        async with api.async_client() as inboxjot:
            await inboxjot.emails.get("em_1")

    with pytest.raises(InboxjotError) as info:
        asyncio.run(run())

    assert info.value.name == "not_found"
    assert len(api.requests) == 3
    assert sleeps[0] == 1


class BrokenBody(httpx.SyncByteStream, httpx.AsyncByteStream):
    def __init__(self, cause: Exception) -> None:
        self.cause = cause

    def __iter__(self) -> Iterator[bytes]:
        yield b'{"id":'
        raise self.cause

    async def __aiter__(self) -> AsyncIterator[bytes]:
        yield b'{"id":'
        raise self.cause


@pytest.mark.parametrize(
    ("cause", "message"),
    [
        (httpx.RemoteProtocolError("peer closed connection"), "Connection error"),
        (httpx.ReadTimeout("timed out"), "Request timed out"),
    ],
)
def test_maps_a_failure_while_reading_the_body(cause: Exception, message: str) -> None:
    api = MockApi(httpx.Response(200, stream=BrokenBody(cause)))
    async_api = MockApi(httpx.Response(200, stream=BrokenBody(cause)))

    with pytest.raises(InboxjotConnectionError, match=message):
        api.client(max_retries=0).emails.get("em_1")

    with pytest.raises(InboxjotConnectionError, match=message):
        asyncio.run(async_api.async_client(max_retries=0).emails.get("em_1"))


@pytest.mark.parametrize("status,name", [(429, "limit_exceeded"), (503, "service_unavailable")])
def test_returns_the_error_when_retry_after_is_over_60_seconds(
    sleeps: list[float], status: int, name: str
) -> None:
    api = MockApi(api_error(status, name, {"Retry-After": "61"}))

    with pytest.raises(InboxjotError) as info:
        api.client().emails.get("em_1")

    assert info.value.status == status
    assert info.value.headers["retry-after"] == "61"
    assert len(api.requests) == 1
    assert sleeps == []


def test_async_client_returns_the_error_when_retry_after_is_over_60_seconds() -> None:
    api = MockApi(api_error(429, "limit_exceeded", {"Retry-After": "3600"}))

    with pytest.raises(InboxjotError):
        asyncio.run(api.async_client().emails.get("em_1"))

    assert len(api.requests) == 1


def test_retries_when_retry_after_is_exactly_60_seconds(sleeps: list[float]) -> None:
    api = MockApi(
        api_error(429, "rate_limit_exceeded", {"Retry-After": "60"}),
        json_reply({"id": "em_1"}),
    )

    assert api.client().emails.get("em_1") == {"id": "em_1"}
    assert sleeps == [60]


def test_caps_the_backoff_at_8_seconds(sleeps: list[float]) -> None:
    api = MockApi(*[api_error(500, "unknown_error") for _ in range(7)])

    with pytest.raises(InboxjotError):
        api.client(max_retries=6).emails.get("em_1")

    assert all(6 <= delay <= 8 for delay in sleeps[4:])


@pytest.mark.parametrize("client_class", [Inboxjot, AsyncInboxjot])
def test_hides_the_api_key_from_debug_output(client_class: type) -> None:
    inboxjot = client_class(api_key="ibx_secret")

    assert "ibx_secret" not in repr(inboxjot)
    assert "ibx_secret" not in str(inboxjot)


def test_sends_a_user_agent_with_the_package_version() -> None:
    api = MockApi(json_reply({}))
    pyproject = (Path(__file__).parent.parent / "pyproject.toml").read_text()
    match = re.search(r'^version = "(.+)"$', pyproject, re.MULTILINE)

    api.client().emails.get("em_1")

    assert match is not None
    assert __version__ == match.group(1)
    assert api.requests[0].headers["User-Agent"] == f"inboxjot-python/{__version__}"
