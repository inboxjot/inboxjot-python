import asyncio
import json

from helpers import MockApi, json_reply

from inboxjot.types import Attachment, Email, SendEmailOptions


def test_sends_an_email_with_auth_json_body_and_idempotency_key() -> None:
    api = MockApi(json_reply({"id": "em_1"}, 202))
    email: SendEmailOptions = {
        "from": "Acme <hi@acme.dev>",
        "to": "jane@acme.dev",
        "subject": "Hi",
        "html": "<p>Hi</p>",
    }

    result = api.client().emails.send(email, idempotency_key="key-1")
    assert result == {"id": "em_1"}

    request = api.requests[0]
    assert str(request.url) == "https://api.test/v1/emails"
    assert request.method == "POST"
    assert request.headers["Authorization"] == "Bearer ibx_test"
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Idempotency-Key"] == "key-1"
    assert json.loads(request.content) == email


def test_maps_each_method_to_its_route() -> None:
    api = MockApi(*[json_reply({}) for _ in range(7)])
    inboxjot = api.client()

    inboxjot.emails.list({"source": "api", "direction": "desc", "per_page": 20})
    inboxjot.emails.batch([{"from": "a@acme.dev", "to": ["b@acme.dev"], "subject": "S"}])
    inboxjot.emails.get("em_1")
    inboxjot.emails.update("em_1", {"scheduled_at": "2026-10-20T09:00:00Z"})
    inboxjot.emails.cancel("em_1")
    inboxjot.emails.list_attachments("em_1")
    inboxjot.emails.get_attachment("em_1", "att 1")

    assert api.routes() == [
        "GET https://api.test/v1/emails?source=api&direction=desc&per_page=20",
        "POST https://api.test/v1/emails/batch",
        "GET https://api.test/v1/emails/em_1",
        "PATCH https://api.test/v1/emails/em_1",
        "POST https://api.test/v1/emails/em_1/cancel",
        "GET https://api.test/v1/emails/em_1/attachments",
        "GET https://api.test/v1/emails/em_1/attachments/att%201",
    ]


def test_sends_no_body_on_reads() -> None:
    api = MockApi(json_reply({}))

    api.client().emails.get_attachment("em_1", "att_1")

    request = api.requests[0]
    assert request.content == b""
    assert "Content-Type" not in request.headers
    assert "Idempotency-Key" not in request.headers


def test_async_client_maps_each_method_to_its_route() -> None:
    api = MockApi(*[json_reply({"id": "em_1"}) for _ in range(8)])

    async def run() -> None:
        async with api.async_client() as inboxjot:
            result = await inboxjot.emails.send({"to": "a@acme.dev"}, idempotency_key="k")
            assert result == {"id": "em_1"}

            await inboxjot.emails.list({"after": "em_0"})
            await inboxjot.emails.batch([{"to": "b@acme.dev"}])
            await inboxjot.emails.get("em_1")
            await inboxjot.emails.update("em_1", {"scheduled_at": "2026-10-20T09:00:00Z"})
            await inboxjot.emails.cancel("em_1")
            await inboxjot.emails.list_attachments("em_1")
            await inboxjot.emails.get_attachment("em_1", "att_1")

    asyncio.run(run())

    assert api.requests[0].headers["Idempotency-Key"] == "k"
    assert api.routes() == [
        "POST https://api.test/v1/emails",
        "GET https://api.test/v1/emails?after=em_0",
        "POST https://api.test/v1/emails/batch",
        "GET https://api.test/v1/emails/em_1",
        "PATCH https://api.test/v1/emails/em_1",
        "POST https://api.test/v1/emails/em_1/cancel",
        "GET https://api.test/v1/emails/em_1/attachments",
        "GET https://api.test/v1/emails/em_1/attachments/att_1",
    ]


def test_sends_a_comma_separated_status() -> None:
    api = MockApi(json_reply({}))

    api.client().emails.list({"status": "delivered,bounced", "status_op": "not", "sort": "to"})

    params = api.requests[0].url.params
    assert params["status"] == "delivered,bounced"
    assert params["status_op"] == "not"
    assert params["sort"] == "to"


def test_decodes_emails() -> None:
    email: Email = {
        "id": "em_1",
        "from": "Acme <hi@acme.dev>",
        "to": ["riti@example.com"],
        "cc": [],
        "bcc": [],
        "subject": "Hi",
        "tags": [{"name": "kind", "value": "welcome"}],
        "status": "delivered",
        "source": "api",
        "scheduled_at": None,
        "sent_at": None,
        "created_at": "2026-10-20T09:00:00Z",
    }
    attachment: Attachment = {
        "id": "att_1",
        "filename": "a.pdf",
        "content_type": "application/pdf",
        "size": 10,
        "content_id": None,
        "content_disposition": "attachment",
        "deleted_at": None,
        "download_url": None,
        "expires_at": None,
    }
    unknown = {**email, "status": "archived", "source": "carrier_pigeon"}
    api = MockApi(json_reply(unknown), json_reply(attachment))
    inboxjot = api.client()

    assert inboxjot.emails.get("em_1") == unknown
    assert inboxjot.emails.get_attachment("em_1", "att_1") == attachment
