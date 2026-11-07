import asyncio
import os
import random
import time
from collections.abc import Mapping
from importlib.metadata import PackageNotFoundError, version
from typing import Any

import httpx

from ._campaigns import AsyncCampaigns, Campaigns
from ._contacts import AsyncContacts, Contacts
from ._domains import AsyncDomains, Domains
from ._emails import AsyncEmails, Emails
from ._errors import InboxjotConnectionError, InboxjotError, read_error
from ._events import AsyncEvents, Events
from ._images import AsyncImages, Images
from ._segments import AsyncSegments, Segments
from ._templates import AsyncTemplates, Templates
from ._topics import AsyncTopics, Topics
from ._webhooks import AsyncWebhooks, Webhooks


def _read_version() -> str:
    try:
        return version("inboxjot")
    except PackageNotFoundError:
        return "dev"


VERSION = _read_version()


def _to_query(params: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if params is None:
        return None

    return {key: value for key, value in params.items() if value is not None}


MAX_RETRY_AFTER_SECONDS = 60


class _BaseClient:
    def __init__(
        self,
        api_key: str | None,
        base_url: str,
        timeout: float,
        max_retries: int,
    ) -> None:
        key = api_key or os.environ.get("INBOXJOT_API_KEY")
        if not key:
            raise ValueError("Missing API key. Pass it to Inboxjot() or set INBOXJOT_API_KEY.")

        self._api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _build_headers(self, idempotency_key: str | None) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._api_key}",
            "User-Agent": f"inboxjot-python/{VERSION}",
        }
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key

        return headers


def _to_error(cause: httpx.TransportError, timeout: float) -> InboxjotConnectionError:
    if isinstance(cause, httpx.TimeoutException):
        return InboxjotConnectionError(f"Request timed out after {timeout}s")

    return InboxjotConnectionError("Connection error")


def _read_retry_after(error: InboxjotError | InboxjotConnectionError) -> float | None:
    if isinstance(error, InboxjotConnectionError):
        return None

    try:
        seconds = float(error.headers.get("retry-after", ""))
    except ValueError:
        return None

    return seconds if seconds >= 0 else None


def _is_retryable(error: InboxjotError | InboxjotConnectionError, is_safe: bool) -> bool:
    if isinstance(error, InboxjotConnectionError):
        return is_safe

    retry_after = _read_retry_after(error)
    if retry_after is not None and retry_after > MAX_RETRY_AFTER_SECONDS:
        return False

    is_rate_limited = error.status == 429
    is_concurrent = error.name == "concurrent_idempotent_requests"
    is_server_error = error.status >= 500

    return is_rate_limited or is_concurrent or (is_server_error and is_safe)


def _get_delay(error: InboxjotError | InboxjotConnectionError, attempt: int) -> float:
    retry_after = _read_retry_after(error)
    if retry_after is not None:
        return retry_after

    backoff = min(0.5 * 2.0**attempt, 8.0)
    jitter = 1 - random.random() * 0.25

    return backoff * jitter


def _check_upload(response: httpx.Response) -> None:
    if not response.is_success:
        error = read_error(response)
        error.message = f"The image upload failed with status {response.status_code}"
        error.args = (error.message,)
        raise error


class Inboxjot(_BaseClient):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = "https://api.inboxjot.com",
        timeout: float = 60.0,
        max_retries: int = 2,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout, max_retries)

        self._http = http_client or httpx.Client()

        self.emails = Emails(self)
        self.contacts = Contacts(self)
        self.events = Events(self)
        self.campaigns = Campaigns(self)
        self.templates = Templates(self)
        self.domains = Domains(self)
        self.images = Images(self)
        self.segments = Segments(self)
        self.topics = Topics(self)
        self.webhooks = Webhooks(self)

    def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        params: Mapping[str, Any] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Any:
        headers = self._build_headers(idempotency_key)
        timeout = self.timeout if timeout is None else timeout
        max_retries = self.max_retries if max_retries is None else max_retries
        is_safe = method in ("GET", "DELETE") or idempotency_key is not None

        attempt = 0
        while True:
            try:
                response = self._http.request(
                    method,
                    self.base_url + path,
                    headers=headers,
                    json=body,
                    params=_to_query(params),
                    timeout=timeout,
                )
            except httpx.TransportError as cause:
                error: InboxjotError | InboxjotConnectionError = _to_error(cause, timeout)
                error.__cause__ = cause
            else:
                if response.is_success:
                    return response.json()

                error = read_error(response)

            if attempt >= max_retries or not _is_retryable(error, is_safe):
                raise error

            time.sleep(_get_delay(error, attempt))
            attempt += 1

    def put(
        self, url: str, body: bytes, content_type: str, *, timeout: float | None = None
    ) -> None:
        timeout = self.timeout if timeout is None else timeout
        try:
            response = self._http.put(
                url, content=body, headers={"Content-Type": content_type}, timeout=timeout
            )
        except httpx.TransportError as cause:
            raise _to_error(cause, timeout) from cause

        _check_upload(response)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Inboxjot":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncInboxjot(_BaseClient):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = "https://api.inboxjot.com",
        timeout: float = 60.0,
        max_retries: int = 2,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout, max_retries)

        self._http = http_client or httpx.AsyncClient()

        self.emails = AsyncEmails(self)
        self.contacts = AsyncContacts(self)
        self.events = AsyncEvents(self)
        self.campaigns = AsyncCampaigns(self)
        self.templates = AsyncTemplates(self)
        self.domains = AsyncDomains(self)
        self.images = AsyncImages(self)
        self.segments = AsyncSegments(self)
        self.topics = AsyncTopics(self)
        self.webhooks = AsyncWebhooks(self)

    async def request(
        self,
        method: str,
        path: str,
        body: Any = None,
        *,
        params: Mapping[str, Any] | None = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Any:
        headers = self._build_headers(idempotency_key)
        timeout = self.timeout if timeout is None else timeout
        max_retries = self.max_retries if max_retries is None else max_retries
        is_safe = method in ("GET", "DELETE") or idempotency_key is not None

        attempt = 0
        while True:
            try:
                response = await self._http.request(
                    method,
                    self.base_url + path,
                    headers=headers,
                    json=body,
                    params=_to_query(params),
                    timeout=timeout,
                )
            except httpx.TransportError as cause:
                error: InboxjotError | InboxjotConnectionError = _to_error(cause, timeout)
                error.__cause__ = cause
            else:
                if response.is_success:
                    return response.json()

                error = read_error(response)

            if attempt >= max_retries or not _is_retryable(error, is_safe):
                raise error

            await asyncio.sleep(_get_delay(error, attempt))
            attempt += 1

    async def put(
        self, url: str, body: bytes, content_type: str, *, timeout: float | None = None
    ) -> None:
        timeout = self.timeout if timeout is None else timeout
        try:
            response = await self._http.put(
                url, content=body, headers={"Content-Type": content_type}, timeout=timeout
            )
        except httpx.TransportError as cause:
            raise _to_error(cause, timeout) from cause

        _check_upload(response)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncInboxjot":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
