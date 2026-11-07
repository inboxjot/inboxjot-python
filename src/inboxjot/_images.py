from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from .types import (
    DeleteImageResponse,
    Image,
    ImageContentType,
    ImagePage,
    ListImagesOptions,
    UploadImageOptions,
)

if TYPE_CHECKING:
    from ._client import AsyncInboxjot, Inboxjot


def _image_path(image_id: str) -> str:
    return f"/v1/images/{quote(image_id, safe='')}"


def _get_content_type(file: bytes) -> ImageContentType:
    if file.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if file.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if file.startswith(b"GIF8"):
        return "image/gif"

    raise ValueError("The image must be a PNG, JPEG or GIF file")


def _create_body(key: str, file_name: str | None) -> dict[str, Any]:
    body = {"key": key}
    if file_name is not None:
        body["file_name"] = file_name

    return body


class Images:
    def __init__(self, client: "Inboxjot") -> None:
        self._client = client

    def list(
        self,
        query: ListImagesOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> ImagePage:
        return self._client.request(
            "GET",
            "/v1/images",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def upload(
        self,
        image: UploadImageOptions,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Image:
        file = image["file"]
        content_type = _get_content_type(file)
        target = self._client.request(
            "POST",
            "/v1/images/presign",
            {"content_type": content_type, "size": len(file)},
            timeout=timeout,
            max_retries=max_retries,
        )
        self._client.put(target["upload_url"], file, content_type, timeout=timeout)

        return self._client.request(
            "POST",
            "/v1/images",
            _create_body(target["key"], image.get("file_name")),
            timeout=timeout,
            max_retries=max_retries,
        )

    def get(
        self,
        image_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Image:
        return self._client.request(
            "GET",
            _image_path(image_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    def delete(
        self,
        image_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteImageResponse:
        return self._client.request(
            "DELETE",
            _image_path(image_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncImages:
    def __init__(self, client: "AsyncInboxjot") -> None:
        self._client = client

    async def list(
        self,
        query: ListImagesOptions | None = None,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> ImagePage:
        return await self._client.request(
            "GET",
            "/v1/images",
            params=query,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def upload(
        self,
        image: UploadImageOptions,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Image:
        file = image["file"]
        content_type = _get_content_type(file)
        target = await self._client.request(
            "POST",
            "/v1/images/presign",
            {"content_type": content_type, "size": len(file)},
            timeout=timeout,
            max_retries=max_retries,
        )
        await self._client.put(target["upload_url"], file, content_type, timeout=timeout)

        return await self._client.request(
            "POST",
            "/v1/images",
            _create_body(target["key"], image.get("file_name")),
            timeout=timeout,
            max_retries=max_retries,
        )

    async def get(
        self,
        image_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Image:
        return await self._client.request(
            "GET",
            _image_path(image_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def delete(
        self,
        image_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> DeleteImageResponse:
        return await self._client.request(
            "DELETE",
            _image_path(image_id),
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
        )
