import json
from typing import Any, cast

import httpx

from .types import ErrorItem, ErrorName


class InboxjotError(Exception):
    def __init__(
        self,
        name: ErrorName,
        status: int,
        message: str,
        errors: list[ErrorItem],
        request_id: str | None,
        headers: httpx.Headers,
    ) -> None:
        super().__init__(message)

        self.name = name
        self.status = status
        self.message = message
        self.errors = errors
        self.request_id = request_id
        self.headers = headers


class InboxjotConnectionError(Exception):
    pass


class WebhookVerificationError(Exception):
    pass


def read_error(response: httpx.Response) -> InboxjotError:
    text = response.text

    try:
        parsed: object = json.loads(text)
    except ValueError:
        parsed = None
    body = cast("dict[str, Any]", parsed) if isinstance(parsed, dict) else {}

    return InboxjotError(
        name=cast(ErrorName, body.get("name") or "unknown_error"),
        status=response.status_code,
        message=body.get("message") or text or f"Request failed with status {response.status_code}",
        errors=body.get("errors") or [],
        request_id=body.get("request_id") or response.headers.get("request-id"),
        headers=response.headers,
    )
