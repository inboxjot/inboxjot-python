import builtins
from typing import TYPE_CHECKING

from .types import BatchEventResponse, SendEventOptions, SendEventResponse

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


class Events:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def send(
        self,
        event: SendEventOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SendEventResponse:
        return self._client.request(
            "POST",
            "/v1/events",
            event,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def batch(
        self,
        events: builtins.list[SendEventOptions],
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> BatchEventResponse:
        return self._client.request(
            "POST",
            "/v1/events/batch",
            events,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncEvents:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def send(
        self,
        event: SendEventOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SendEventResponse:
        return await self._client.request(
            "POST",
            "/v1/events",
            event,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def batch(
        self,
        events: builtins.list[SendEventOptions],
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> BatchEventResponse:
        return await self._client.request(
            "POST",
            "/v1/events/batch",
            events,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
