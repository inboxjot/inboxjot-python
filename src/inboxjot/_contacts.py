from typing import TYPE_CHECKING
from urllib.parse import quote

from .types import (
    Contact,
    ContactPage,
    CreateContactOptions,
    CreateContactResponse,
    DeleteContactResponse,
    EraseContactOptions,
    EraseContactResponse,
    ListContactsOptions,
    UpdateContactOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _contact_path(contact_id_or_email: str) -> str:
    return f"/v1/contacts/{quote(contact_id_or_email, safe='')}"


class Contacts:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListContactsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> ContactPage:
        return self._client.request(
            "GET",
            "/v1/contacts",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        contact: CreateContactOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CreateContactResponse:
        return self._client.request(
            "POST",
            "/v1/contacts",
            contact,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        contact_id_or_email: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Contact:
        return self._client.request(
            "GET",
            _contact_path(contact_id_or_email),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        contact_id_or_email: str,
        contact: UpdateContactOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Contact:
        return self._client.request(
            "PATCH",
            _contact_path(contact_id_or_email),
            contact,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        contact_id_or_email: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteContactResponse:
        return self._client.request(
            "DELETE",
            _contact_path(contact_id_or_email),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def erase(
        self,
        contact: EraseContactOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> EraseContactResponse:
        return self._client.request(
            "POST",
            "/v1/contacts/erase",
            contact,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncContacts:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListContactsOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> ContactPage:
        return await self._client.request(
            "GET",
            "/v1/contacts",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        contact: CreateContactOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CreateContactResponse:
        return await self._client.request(
            "POST",
            "/v1/contacts",
            contact,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        contact_id_or_email: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Contact:
        return await self._client.request(
            "GET",
            _contact_path(contact_id_or_email),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        contact_id_or_email: str,
        contact: UpdateContactOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Contact:
        return await self._client.request(
            "PATCH",
            _contact_path(contact_id_or_email),
            contact,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        contact_id_or_email: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteContactResponse:
        return await self._client.request(
            "DELETE",
            _contact_path(contact_id_or_email),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def erase(
        self,
        contact: EraseContactOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> EraseContactResponse:
        return await self._client.request(
            "POST",
            "/v1/contacts/erase",
            contact,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
