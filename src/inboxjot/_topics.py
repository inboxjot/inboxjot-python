from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    CreateTopicOptions,
    DeleteTopicResponse,
    ListTopicsOptions,
    Topic,
    TopicPage,
    UpdateTopicOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _topic_path(topic_id: str) -> str:
    return f"/v1/topics/{quote(topic_id, safe='')}"


class Topics:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListTopicsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TopicPage:
        return self._client.request(
            "GET",
            "/v1/topics",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        topic: CreateTopicOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Topic:
        return self._client.request(
            "POST",
            "/v1/topics",
            topic,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        topic_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Topic:
        return self._client.request(
            "GET",
            _topic_path(topic_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        topic_id: str,
        topic: UpdateTopicOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Topic:
        return self._client.request(
            "PATCH",
            _topic_path(topic_id),
            topic,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        topic_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteTopicResponse:
        return self._client.request(
            "DELETE",
            _topic_path(topic_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncTopics:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListTopicsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TopicPage:
        return await self._client.request(
            "GET",
            "/v1/topics",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        topic: CreateTopicOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Topic:
        return await self._client.request(
            "POST",
            "/v1/topics",
            topic,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        topic_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Topic:
        return await self._client.request(
            "GET",
            _topic_path(topic_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        topic_id: str,
        topic: UpdateTopicOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Topic:
        return await self._client.request(
            "PATCH",
            _topic_path(topic_id),
            topic,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        topic_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteTopicResponse:
        return await self._client.request(
            "DELETE",
            _topic_path(topic_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
