import asyncio

import httpx
import pytest
from helpers import MockApi, check_routes, json_reply, read_body

from inboxjot import InboxjotError
from inboxjot.types import Image, ImagePage

BASE = "https://api.test/v1/images"
PNG = b"\x89PNG\r\n\x1a\n\x01\x02"
TARGET = {"upload_url": "https://r2.test/put?sig=1", "key": "image-uploads/ws_a/1"}


def upload_replies() -> list[httpx.Response]:
    return [json_reply(TARGET), httpx.Response(200), json_reply({"id": "img_1"}, 201)]


def test_maps_each_method_to_its_route() -> None:
    check_routes(
        [
            (lambda i: i.images.list({"type": "png"}), f"GET {BASE}?type=png"),
            (lambda i: i.images.get("img_1"), f"GET {BASE}/img_1"),
            (lambda i: i.images.delete("img_1"), f"DELETE {BASE}/img_1"),
        ]
    )


def test_decodes_images() -> None:
    image: Image = {
        "id": "img_1",
        "file_name": "a.png",
        "url": None,
        "content_type": "image/png",
        "size_bytes": 10,
        "width": 1,
        "height": 1,
        "creator_name": None,
        "created_at": "2026-10-20T09:00:00Z",
    }
    page: ImagePage = {"data": [image], "total": 1, "next_cursor": None, "prev_cursor": None}
    unknown = {**image, "content_type": "image/webp"}
    api = MockApi(json_reply(unknown), json_reply(page))
    inboxjot = api.client()

    assert inboxjot.images.get("img_1") == unknown
    assert inboxjot.images.list() == page


def check_upload(api: MockApi, image: Image) -> None:
    assert image == {"id": "img_1"}
    assert api.routes() == [
        f"POST {BASE}/presign",
        "PUT https://r2.test/put?sig=1",
        f"POST {BASE}",
    ]
    presign, put, create = api.requests
    assert read_body(presign) == {"content_type": "image/png", "size": 10}
    assert put.headers["content-type"] == "image/png"
    assert "authorization" not in put.headers
    assert put.content == PNG
    assert read_body(create) == {"key": TARGET["key"], "file_name": "logo.png"}


def test_uploads_the_file_and_adds_the_image() -> None:
    api = MockApi(*upload_replies())

    check_upload(api, api.client().images.upload({"file": PNG, "file_name": "logo.png"}))


def test_async_uploads_the_file_and_adds_the_image() -> None:
    api = MockApi(*upload_replies())

    async def run() -> Image:
        async with api.async_client() as inboxjot:
            return await inboxjot.images.upload({"file": PNG, "file_name": "logo.png"})

    check_upload(api, asyncio.run(run()))


@pytest.mark.parametrize(
    ("file", "content_type"),
    [(b"\xff\xd8\xff\xe0", "image/jpeg"), (b"GIF89a", "image/gif")],
)
def test_detects_jpeg_and_gif(file: bytes, content_type: str) -> None:
    api = MockApi(*upload_replies())
    async_api = MockApi(*upload_replies())

    api.client().images.upload({"file": file})

    async def run() -> None:
        async with async_api.async_client() as inboxjot:
            await inboxjot.images.upload({"file": file})

    asyncio.run(run())

    for request in (api.requests[0], async_api.requests[0]):
        assert read_body(request)["content_type"] == content_type
    assert read_body(api.requests[2]) == {"key": TARGET["key"]}


def test_refuses_a_file_that_is_not_an_image_before_any_request() -> None:
    api = MockApi()
    message = "The image must be a PNG, JPEG or GIF file"

    with pytest.raises(ValueError, match=message):
        api.client().images.upload({"file": b"\x01\x02\x03"})

    async def run() -> None:
        async with api.async_client() as inboxjot:
            await inboxjot.images.upload({"file": b"\x01\x02\x03"})

    with pytest.raises(ValueError, match=message):
        asyncio.run(run())

    assert api.requests == []


def test_throws_when_storage_rejects_the_upload() -> None:
    def replies() -> list[httpx.Response]:
        return [
            json_reply(TARGET),
            httpx.Response(403, text="<Error>SignatureDoesNotMatch</Error>"),
        ]

    api = MockApi(*replies())
    async_api = MockApi(*replies())

    with pytest.raises(InboxjotError) as sync_error:
        api.client().images.upload({"file": PNG})

    async def run() -> None:
        async with async_api.async_client() as inboxjot:
            await inboxjot.images.upload({"file": PNG})

    with pytest.raises(InboxjotError) as async_error:
        asyncio.run(run())

    for error in (sync_error.value, async_error.value):
        assert error.status == 403
        assert error.message == "The image upload failed with status 403"
    assert len(api.requests) == 2
    assert len(async_api.requests) == 2
