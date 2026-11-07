from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    CreateDomainOptions,
    DeleteDomainResponse,
    Domain,
    DomainPage,
    ListDomainsOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _domain_path(domain_id: str) -> str:
    return f"/v1/domains/{quote(domain_id, safe='')}"


class Domains:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListDomainsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DomainPage:
        return self._client.request(
            "GET",
            "/v1/domains",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        domain: CreateDomainOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Domain:
        return self._client.request(
            "POST",
            "/v1/domains",
            domain,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        domain_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Domain:
        return self._client.request(
            "GET",
            _domain_path(domain_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        domain_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteDomainResponse:
        return self._client.request(
            "DELETE",
            _domain_path(domain_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def verify(
        self,
        domain_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Domain:
        return self._client.request(
            "POST",
            f"{_domain_path(domain_id)}/verify",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncDomains:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListDomainsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DomainPage:
        return await self._client.request(
            "GET",
            "/v1/domains",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        domain: CreateDomainOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Domain:
        return await self._client.request(
            "POST",
            "/v1/domains",
            domain,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        domain_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Domain:
        return await self._client.request(
            "GET",
            _domain_path(domain_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        domain_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteDomainResponse:
        return await self._client.request(
            "DELETE",
            _domain_path(domain_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def verify(
        self,
        domain_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Domain:
        return await self._client.request(
            "POST",
            f"{_domain_path(domain_id)}/verify",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
