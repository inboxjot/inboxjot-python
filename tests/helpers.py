import asyncio
import json
from collections.abc import Callable
from typing import Any

import httpx

from inboxjot import AsyncInboxjot, Inboxjot

Reply = httpx.Response | Exception
Route = tuple[Callable[[Any], Any], str]


def json_reply(
    body: Any, status: int = 200, headers: dict[str, str] | None = None
) -> httpx.Response:
    return httpx.Response(status, json=body, headers=headers)


def api_error(status: int, name: str, headers: dict[str, str] | None = None) -> httpx.Response:
    body: dict[str, Any] = {
        "name": name,
        "status": status,
        "message": f"{name} message",
        "errors": [],
        "request_id": "req_1",
    }

    return json_reply(body, status, headers)


class MockApi:
    def __init__(self, *replies: Reply) -> None:
        self.replies = list(replies)
        self.requests: list[httpx.Request] = []

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)

        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply

        return reply

    def client(self, max_retries: int = 2) -> Inboxjot:
        http_client = httpx.Client(transport=httpx.MockTransport(self.handle))

        return Inboxjot(
            api_key="ibx_test",
            base_url="https://api.test/",
            max_retries=max_retries,
            http_client=http_client,
        )

    def async_client(self, max_retries: int = 2) -> AsyncInboxjot:
        http_client = httpx.AsyncClient(transport=httpx.MockTransport(self.handle))

        return AsyncInboxjot(
            api_key="ibx_test",
            base_url="https://api.test/",
            max_retries=max_retries,
            http_client=http_client,
        )

    def routes(self) -> list[str]:
        return [f"{request.method} {request.url}" for request in self.requests]


def check_routes(routes: list[Route]) -> None:
    api = MockApi(*[json_reply({}) for _ in routes])
    async_api = MockApi(*[json_reply({}) for _ in routes])
    inboxjot = api.client()
    expected = [route for _, route in routes]

    for call, _ in routes:
        call(inboxjot)

    async def run() -> None:
        async with async_api.async_client() as async_inboxjot:
            for call, _ in routes:
                await call(async_inboxjot)

    asyncio.run(run())

    assert api.routes() == expected
    assert async_api.routes() == expected


def read_body(request: httpx.Request) -> Any:
    return json.loads(request.content)
