import builtins
from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    Attachment,
    AttachmentList,
    BatchEmailOptions,
    BatchEmailResponse,
    CancelEmailResponse,
    Email,
    EmailPage,
    ListEmailsOptions,
    SendEmailOptions,
    SendEmailResponse,
    UpdateEmailOptions,
    UpdateEmailResponse,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _email_path(email_id: str) -> str:
    return f"/v1/emails/{quote(email_id, safe='')}"


def _attachment_path(email_id: str, attachment_id: str) -> str:
    return f"{_email_path(email_id)}/attachments/{quote(attachment_id, safe='')}"


class Emails:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListEmailsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> EmailPage:
        return self._client.request(
            "GET",
            "/v1/emails",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def send(
        self,
        email: SendEmailOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SendEmailResponse:
        return self._client.request(
            "POST",
            "/v1/emails",
            email,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def batch(
        self,
        emails: builtins.list[BatchEmailOptions],
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> BatchEmailResponse:
        return self._client.request(
            "POST",
            "/v1/emails/batch",
            emails,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        email_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Email:
        return self._client.request(
            "GET",
            _email_path(email_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        email_id: str,
        email: UpdateEmailOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> UpdateEmailResponse:
        return self._client.request(
            "PATCH",
            _email_path(email_id),
            email,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def cancel(
        self,
        email_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CancelEmailResponse:
        return self._client.request(
            "POST",
            f"{_email_path(email_id)}/cancel",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_attachments(
        self,
        email_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AttachmentList:
        return self._client.request(
            "GET",
            f"{_email_path(email_id)}/attachments",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get_attachment(
        self,
        email_id: str,
        attachment_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Attachment:
        return self._client.request(
            "GET",
            _attachment_path(email_id, attachment_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncEmails:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListEmailsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> EmailPage:
        return await self._client.request(
            "GET",
            "/v1/emails",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def send(
        self,
        email: SendEmailOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> SendEmailResponse:
        return await self._client.request(
            "POST",
            "/v1/emails",
            email,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def batch(
        self,
        emails: builtins.list[BatchEmailOptions],
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> BatchEmailResponse:
        return await self._client.request(
            "POST",
            "/v1/emails/batch",
            emails,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        email_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Email:
        return await self._client.request(
            "GET",
            _email_path(email_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        email_id: str,
        email: UpdateEmailOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> UpdateEmailResponse:
        return await self._client.request(
            "PATCH",
            _email_path(email_id),
            email,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def cancel(
        self,
        email_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CancelEmailResponse:
        return await self._client.request(
            "POST",
            f"{_email_path(email_id)}/cancel",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list_attachments(
        self,
        email_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AttachmentList:
        return await self._client.request(
            "GET",
            f"{_email_path(email_id)}/attachments",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get_attachment(
        self,
        email_id: str,
        attachment_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Attachment:
        return await self._client.request(
            "GET",
            _attachment_path(email_id, attachment_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
