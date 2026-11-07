import asyncio

from helpers import MockApi, json_reply, read_body

from inboxjot.types import Contact, ContactPage


def test_maps_each_method_to_its_route() -> None:
    api = MockApi(*[json_reply({}) for _ in range(5)])
    inboxjot = api.client()

    inboxjot.contacts.list({"status": "subscribed", "segment_id": "sg_1", "per_page": 10})
    inboxjot.contacts.create({"email": "jane@acme.dev", "first_name": "Jane"})
    inboxjot.contacts.get("ct_1")
    inboxjot.contacts.update(
        "ct_1",
        {"last_name": "Doe", "topics": [{"id": "tp_1", "status": "unsubscribed"}]},
    )
    inboxjot.contacts.delete("ct_1")

    assert api.routes() == [
        "GET https://api.test/v1/contacts?status=subscribed&segment_id=sg_1&per_page=10",
        "POST https://api.test/v1/contacts",
        "GET https://api.test/v1/contacts/ct_1",
        "PATCH https://api.test/v1/contacts/ct_1",
        "DELETE https://api.test/v1/contacts/ct_1",
    ]


def test_encodes_an_email_address_as_the_contact_id() -> None:
    api = MockApi(json_reply({}))

    api.client().contacts.get("jane+news@acme.dev")

    assert api.routes() == ["GET https://api.test/v1/contacts/jane%2Bnews%40acme.dev"]


def test_erases_by_email_and_returns_the_queued_status() -> None:
    api = MockApi(json_reply({"status": "queued"}, 202))

    result = api.client().contacts.erase({"email": "jane@acme.dev"})

    assert result == {"status": "queued"}
    assert api.routes() == ["POST https://api.test/v1/contacts/erase"]
    assert read_body(api.requests[0]) == {"email": "jane@acme.dev"}


def test_deletes_a_contact_without_an_erase_option() -> None:
    api = MockApi(json_reply({"status": "ok"}))

    assert api.client().contacts.delete("ct_1") == {"status": "ok"}
    assert api.routes() == ["DELETE https://api.test/v1/contacts/ct_1"]


def test_decodes_contacts() -> None:
    contact: Contact = {
        "id": "ct_1",
        "email": "riti@example.com",
        "first_name": None,
        "last_name": None,
        "status": "subscribed",
        "language": "en",
        "properties": {"plan": "pro", "seats": 3, "beta": True, "note": None},
        "segments": [{"id": "sg_1", "name": "Beta"}],
        "topics": [{"id": "tp_1", "name": "News", "status": None, "subscribed": False}],
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    page: ContactPage = {
        "data": [
            {
                "id": "ct_1",
                "email": "riti@example.com",
                "first_name": None,
                "last_name": None,
                "properties": {},
                "status": "pending",
                "is_suppressed": False,
                "segments": [],
                "last_activity": None,
                "created_at": "2026-10-20T09:00:00Z",
            }
        ],
        "total": 1,
        "next_cursor": None,
        "prev_cursor": None,
    }
    unknown = {**contact, "status": "archived"}
    api = MockApi(json_reply(unknown), json_reply(page))
    inboxjot = api.client()

    assert inboxjot.contacts.get("ct_1") == unknown
    assert inboxjot.contacts.list() == page


def test_async_client_maps_each_method_to_its_route() -> None:
    api = MockApi(*[json_reply({}) for _ in range(6)])

    async def run() -> None:
        async with api.async_client() as inboxjot:
            await inboxjot.contacts.list()
            await inboxjot.contacts.create({"email": "jane@acme.dev"})
            await inboxjot.contacts.get("ct_1")
            await inboxjot.contacts.update("ct_1", {"last_name": "Doe"})
            await inboxjot.contacts.delete("ct_1")
            await inboxjot.contacts.erase({"email": "jane@acme.dev"})

    asyncio.run(run())

    assert api.routes() == [
        "GET https://api.test/v1/contacts",
        "POST https://api.test/v1/contacts",
        "GET https://api.test/v1/contacts/ct_1",
        "PATCH https://api.test/v1/contacts/ct_1",
        "DELETE https://api.test/v1/contacts/ct_1",
        "POST https://api.test/v1/contacts/erase",
    ]


def test_leaves_out_empty_cursors_from_the_query() -> None:
    api = MockApi(json_reply({"data": [], "total": 0, "next_cursor": None, "prev_cursor": None}))

    api.client().contacts.list({"after": None, "before": None, "per_page": 1})

    assert str(api.requests[0].url) == "https://api.test/v1/contacts?per_page=1"
