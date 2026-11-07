from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    AddSegmentMembersResponse,
    CreateSegmentOptions,
    DeleteSegmentResponse,
    ListSegmentMembersOptions,
    ListSegmentsOptions,
    RemoveSegmentMembersResponse,
    Segment,
    SegmentMemberPage,
    SegmentMembersOptions,
    SegmentPage,
    UpdateSegmentOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _segment_path(segment_id: str) -> str:
    return f"/v1/segments/{quote(segment_id, safe='')}"


class Segments:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListSegmentsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SegmentPage:
        return self._client.request(
            "GET",
            "/v1/segments",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        segment: CreateSegmentOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Segment:
        return self._client.request(
            "POST",
            "/v1/segments",
            segment,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        segment_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Segment:
        return self._client.request(
            "GET",
            _segment_path(segment_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        segment_id: str,
        segment: UpdateSegmentOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Segment:
        return self._client.request(
            "PATCH",
            _segment_path(segment_id),
            segment,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        segment_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteSegmentResponse:
        return self._client.request(
            "DELETE",
            _segment_path(segment_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_members(
        self,
        segment_id: str,
        query: ListSegmentMembersOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SegmentMemberPage:
        return self._client.request(
            "GET",
            f"{_segment_path(segment_id)}/members",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def add_members(
        self,
        segment_id: str,
        members: SegmentMembersOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AddSegmentMembersResponse:
        return self._client.request(
            "POST",
            f"{_segment_path(segment_id)}/members",
            members,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def remove_members(
        self,
        segment_id: str,
        members: SegmentMembersOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> RemoveSegmentMembersResponse:
        return self._client.request(
            "DELETE",
            f"{_segment_path(segment_id)}/members",
            members,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncSegments:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListSegmentsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SegmentPage:
        return await self._client.request(
            "GET",
            "/v1/segments",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        segment: CreateSegmentOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Segment:
        return await self._client.request(
            "POST",
            "/v1/segments",
            segment,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        segment_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Segment:
        return await self._client.request(
            "GET",
            _segment_path(segment_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        segment_id: str,
        segment: UpdateSegmentOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Segment:
        return await self._client.request(
            "PATCH",
            _segment_path(segment_id),
            segment,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        segment_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteSegmentResponse:
        return await self._client.request(
            "DELETE",
            _segment_path(segment_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list_members(
        self,
        segment_id: str,
        query: ListSegmentMembersOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SegmentMemberPage:
        return await self._client.request(
            "GET",
            f"{_segment_path(segment_id)}/members",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def add_members(
        self,
        segment_id: str,
        members: SegmentMembersOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AddSegmentMembersResponse:
        return await self._client.request(
            "POST",
            f"{_segment_path(segment_id)}/members",
            members,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def remove_members(
        self,
        segment_id: str,
        members: SegmentMembersOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> RemoveSegmentMembersResponse:
        return await self._client.request(
            "DELETE",
            f"{_segment_path(segment_id)}/members",
            members,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
