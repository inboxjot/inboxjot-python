from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    Brand,
    BrandPage,
    CreateBrandOptions,
    DeleteBrandResponse,
    ListBrandsOptions,
    UpdateBrandOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _brand_path(brand_id: str) -> str:
    return f"/v1/brands/{quote(brand_id, safe='')}"


class Brands:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListBrandsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> BrandPage:
        return self._client.request(
            "GET",
            "/v1/brands",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        brand: CreateBrandOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Brand:
        return self._client.request(
            "POST",
            "/v1/brands",
            brand,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        brand_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Brand:
        return self._client.request(
            "GET",
            _brand_path(brand_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        brand_id: str,
        brand: UpdateBrandOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Brand:
        return self._client.request(
            "PATCH",
            _brand_path(brand_id),
            brand,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        brand_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteBrandResponse:
        return self._client.request(
            "DELETE",
            _brand_path(brand_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncBrands:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListBrandsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> BrandPage:
        return await self._client.request(
            "GET",
            "/v1/brands",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        brand: CreateBrandOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Brand:
        return await self._client.request(
            "POST",
            "/v1/brands",
            brand,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        brand_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Brand:
        return await self._client.request(
            "GET",
            _brand_path(brand_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        brand_id: str,
        brand: UpdateBrandOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Brand:
        return await self._client.request(
            "PATCH",
            _brand_path(brand_id),
            brand,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        brand_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteBrandResponse:
        return await self._client.request(
            "DELETE",
            _brand_path(brand_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
