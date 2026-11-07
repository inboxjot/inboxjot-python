from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    Campaign,
    CampaignPage,
    CampaignVersion,
    CampaignVersionDetail,
    CampaignVersionPage,
    CreateCampaignOptions,
    CreateCampaignVersionOptions,
    DeleteCampaignResponse,
    ListCampaignsOptions,
    ListCampaignVersionsOptions,
    SendCampaignOptions,
    SendCampaignTestOptions,
    SendCampaignTestResponse,
    UpdateCampaignOptions,
    UpdateCampaignVersionOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _campaign_path(campaign_id: str) -> str:
    return f"/v1/campaigns/{quote(campaign_id, safe='')}"


def _version_path(campaign_id: str, version_id: str) -> str:
    return f"{_campaign_path(campaign_id)}/versions/{quote(version_id, safe='')}"


class Campaigns:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListCampaignsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignPage:
        return self._client.request(
            "GET",
            "/v1/campaigns",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        campaign: CreateCampaignOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return self._client.request(
            "POST",
            "/v1/campaigns",
            campaign,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        campaign_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return self._client.request(
            "GET",
            _campaign_path(campaign_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        campaign_id: str,
        campaign: UpdateCampaignOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return self._client.request(
            "PATCH",
            _campaign_path(campaign_id),
            campaign,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        campaign_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteCampaignResponse:
        return self._client.request(
            "DELETE",
            _campaign_path(campaign_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def send(
        self,
        campaign_id: str,
        campaign: SendCampaignOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/send",
            campaign or {},
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def cancel(
        self,
        campaign_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/cancel",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def send_test(
        self,
        campaign_id: str,
        test: SendCampaignTestOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SendCampaignTestResponse:
        return self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/test",
            test,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_versions(
        self,
        campaign_id: str,
        query: ListCampaignVersionsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersionPage:
        return self._client.request(
            "GET",
            f"{_campaign_path(campaign_id)}/versions",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create_version(
        self,
        campaign_id: str,
        version: CreateCampaignVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersion:
        return self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/versions",
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get_version(
        self,
        campaign_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersionDetail:
        return self._client.request(
            "GET",
            _version_path(campaign_id, version_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update_version(
        self,
        campaign_id: str,
        version_id: str,
        version: UpdateCampaignVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersion:
        return self._client.request(
            "PATCH",
            _version_path(campaign_id, version_id),
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def restore_version(
        self,
        campaign_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return self._client.request(
            "POST",
            f"{_version_path(campaign_id, version_id)}/restore",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncCampaigns:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListCampaignsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignPage:
        return await self._client.request(
            "GET",
            "/v1/campaigns",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        campaign: CreateCampaignOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return await self._client.request(
            "POST",
            "/v1/campaigns",
            campaign,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        campaign_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return await self._client.request(
            "GET",
            _campaign_path(campaign_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        campaign_id: str,
        campaign: UpdateCampaignOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return await self._client.request(
            "PATCH",
            _campaign_path(campaign_id),
            campaign,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        campaign_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteCampaignResponse:
        return await self._client.request(
            "DELETE",
            _campaign_path(campaign_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def send(
        self,
        campaign_id: str,
        campaign: SendCampaignOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return await self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/send",
            campaign or {},
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def cancel(
        self,
        campaign_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return await self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/cancel",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def send_test(
        self,
        campaign_id: str,
        test: SendCampaignTestOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SendCampaignTestResponse:
        return await self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/test",
            test,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list_versions(
        self,
        campaign_id: str,
        query: ListCampaignVersionsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersionPage:
        return await self._client.request(
            "GET",
            f"{_campaign_path(campaign_id)}/versions",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create_version(
        self,
        campaign_id: str,
        version: CreateCampaignVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersion:
        return await self._client.request(
            "POST",
            f"{_campaign_path(campaign_id)}/versions",
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get_version(
        self,
        campaign_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersionDetail:
        return await self._client.request(
            "GET",
            _version_path(campaign_id, version_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update_version(
        self,
        campaign_id: str,
        version_id: str,
        version: UpdateCampaignVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CampaignVersion:
        return await self._client.request(
            "PATCH",
            _version_path(campaign_id, version_id),
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def restore_version(
        self,
        campaign_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Campaign:
        return await self._client.request(
            "POST",
            f"{_version_path(campaign_id, version_id)}/restore",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
