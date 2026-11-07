import base64
import hashlib
import hmac
import json
import time
from collections.abc import Mapping
from typing import TYPE_CHECKING
from urllib.parse import quote

from ._errors import WebhookVerificationError
from .types import (
    CreateWebhookOptions,
    CreateWebhookResponse,
    DeleteWebhookResponse,
    ListWebhooksOptions,
    UpdateWebhookOptions,
    UpdateWebhookResponse,
    Webhook,
    WebhookEvent,
    WebhookPage,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot

TOLERANCE_SECONDS = 300


def _webhook_path(endpoint_id: str) -> str:
    return f"/v1/webhooks/{quote(endpoint_id, safe='')}"


class Webhooks:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListWebhooksOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> WebhookPage:
        return self._client.request(
            "GET",
            "/v1/webhooks",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def create(
        self,
        webhook: CreateWebhookOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CreateWebhookResponse:
        return self._client.request(
            "POST",
            "/v1/webhooks",
            webhook,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        endpoint_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Webhook:
        return self._client.request(
            "GET",
            _webhook_path(endpoint_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def update(
        self,
        endpoint_id: str,
        webhook: UpdateWebhookOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> UpdateWebhookResponse:
        return self._client.request(
            "PATCH",
            _webhook_path(endpoint_id),
            webhook,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        endpoint_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteWebhookResponse:
        return self._client.request(
            "DELETE",
            _webhook_path(endpoint_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def verify(
        self,
        *,
        payload: str | bytes,
        headers: Mapping[str, str],
        secret: str,
    ) -> WebhookEvent:
        return verify_webhook(payload=payload, headers=headers, secret=secret)


class AsyncWebhooks:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListWebhooksOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> WebhookPage:
        return await self._client.request(
            "GET",
            "/v1/webhooks",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def create(
        self,
        webhook: CreateWebhookOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> CreateWebhookResponse:
        return await self._client.request(
            "POST",
            "/v1/webhooks",
            webhook,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        endpoint_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Webhook:
        return await self._client.request(
            "GET",
            _webhook_path(endpoint_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def update(
        self,
        endpoint_id: str,
        webhook: UpdateWebhookOptions,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> UpdateWebhookResponse:
        return await self._client.request(
            "PATCH",
            _webhook_path(endpoint_id),
            webhook,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        endpoint_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteWebhookResponse:
        return await self._client.request(
            "DELETE",
            _webhook_path(endpoint_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def verify(
        self,
        *,
        payload: str | bytes,
        headers: Mapping[str, str],
        secret: str,
    ) -> WebhookEvent:
        return verify_webhook(payload=payload, headers=headers, secret=secret)


def verify_webhook(
    *,
    payload: str | bytes,
    headers: Mapping[str, str],
    secret: str,
) -> WebhookEvent:
    webhook_id = _read_header(headers, "webhook-id")
    timestamp = _read_header(headers, "webhook-timestamp")
    signatures = _read_header(headers, "webhook-signature")
    if not webhook_id or not timestamp or not signatures:
        raise WebhookVerificationError("Missing webhook headers")

    try:
        seconds = int(timestamp)
    except ValueError:
        raise WebhookVerificationError("Invalid webhook timestamp") from None

    if abs(int(time.time()) - seconds) > TOLERANCE_SECONDS:
        raise WebhookVerificationError("Webhook timestamp is outside the tolerance")

    key = _decode_base64(secret.removeprefix("whsec_"))
    if not key:
        raise WebhookVerificationError("Invalid webhook secret")

    body = payload.encode() if isinstance(payload, str) else payload
    content = f"{webhook_id}.{timestamp}.".encode() + body
    expected = hmac.new(key, content, hashlib.sha256).digest()

    for signature in signatures.split(" "):
        version, _, value = signature.partition(",")
        if version != "v1" or not value:
            continue

        decoded = _decode_base64(value)
        if decoded is not None and hmac.compare_digest(decoded, expected):
            return json.loads(body)

    raise WebhookVerificationError("No matching signature found")


def _read_header(headers: Mapping[str, str], name: str) -> str | None:
    return next((value for key, value in headers.items() if key.lower() == name), None)


def _decode_base64(text: str) -> bytes | None:
    try:
        return base64.b64decode(text, validate=True)
    except ValueError:
        return None
