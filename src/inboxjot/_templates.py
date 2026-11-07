from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    CreateTemplateOptions,
    CreateTemplateVersionOptions,
    DeleteTemplateResponse,
    ListTemplatesOptions,
    ListTemplateVersionsOptions,
    Template,
    TemplatePage,
    TemplateVersion,
    TemplateVersionDetail,
    TemplateVersionPage,
    UpdateTemplateOptions,
    UpdateTemplateVersionOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _template_path(template_id: str) -> str:
    return f"/v1/templates/{quote(template_id, safe='')}"


def _version_path(template_id: str, version_id: str) -> str:
    return f"{_template_path(template_id)}/versions/{quote(version_id, safe='')}"


class Templates:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListTemplatesOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplatePage:
        return self._client.request(
            "GET",
            "/v1/templates",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        template: CreateTemplateOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return self._client.request(
            "POST",
            "/v1/templates",
            template,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        template_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return self._client.request(
            "GET",
            _template_path(template_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        template_id: str,
        template: UpdateTemplateOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return self._client.request(
            "PATCH",
            _template_path(template_id),
            template,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        template_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteTemplateResponse:
        return self._client.request(
            "DELETE",
            _template_path(template_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def publish(
        self,
        template_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return self._client.request(
            "POST",
            f"{_template_path(template_id)}/publish",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_versions(
        self,
        template_id: str,
        query: ListTemplateVersionsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersionPage:
        return self._client.request(
            "GET",
            f"{_template_path(template_id)}/versions",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create_version(
        self,
        template_id: str,
        version: CreateTemplateVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersion:
        return self._client.request(
            "POST",
            f"{_template_path(template_id)}/versions",
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get_version(
        self,
        template_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersionDetail:
        return self._client.request(
            "GET",
            _version_path(template_id, version_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update_version(
        self,
        template_id: str,
        version_id: str,
        version: UpdateTemplateVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersion:
        return self._client.request(
            "PATCH",
            _version_path(template_id, version_id),
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def restore_version(
        self,
        template_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return self._client.request(
            "POST",
            f"{_version_path(template_id, version_id)}/restore",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncTemplates:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListTemplatesOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplatePage:
        return await self._client.request(
            "GET",
            "/v1/templates",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        template: CreateTemplateOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return await self._client.request(
            "POST",
            "/v1/templates",
            template,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        template_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return await self._client.request(
            "GET",
            _template_path(template_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        template_id: str,
        template: UpdateTemplateOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return await self._client.request(
            "PATCH",
            _template_path(template_id),
            template,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        template_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteTemplateResponse:
        return await self._client.request(
            "DELETE",
            _template_path(template_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def publish(
        self,
        template_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return await self._client.request(
            "POST",
            f"{_template_path(template_id)}/publish",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list_versions(
        self,
        template_id: str,
        query: ListTemplateVersionsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersionPage:
        return await self._client.request(
            "GET",
            f"{_template_path(template_id)}/versions",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create_version(
        self,
        template_id: str,
        version: CreateTemplateVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersion:
        return await self._client.request(
            "POST",
            f"{_template_path(template_id)}/versions",
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get_version(
        self,
        template_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersionDetail:
        return await self._client.request(
            "GET",
            _version_path(template_id, version_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update_version(
        self,
        template_id: str,
        version_id: str,
        version: UpdateTemplateVersionOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> TemplateVersion:
        return await self._client.request(
            "PATCH",
            _version_path(template_id, version_id),
            version,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def restore_version(
        self,
        template_id: str,
        version_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Template:
        return await self._client.request(
            "POST",
            f"{_version_path(template_id, version_id)}/restore",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
