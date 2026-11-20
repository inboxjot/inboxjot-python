import asyncio
import json

from helpers import MockApi, json_reply

from inboxjot.types import SendEventOptions


def test_maps_send_to_its_route() -> None:
    api = MockApi(json_reply({"contact_id": "ct_1"}))
    event: SendEventOptions = {
        "event": "signed_up",
        "email": "jane@acme.dev",
        "properties": {"plan": "pro"},
    }

    result = api.client().events.send(event)

    assert result == {"contact_id": "ct_1"}
    assert api.routes() == ["POST https://api.test/v1/events"]
    assert json.loads(api.requests[0].content) == event


def test_async_client_maps_send_to_its_route() -> None:
    api = MockApi(json_reply({"contact_id": "ct_1"}))

    async def run() -> None:
        async with api.async_client() as inboxjot:
            await inboxjot.events.send({"event": "signed_up", "email": "jane@acme.dev"})

    asyncio.run(run())

    assert api.routes() == ["POST https://api.test/v1/events"]


def test_maps_batch_to_its_route() -> None:
    api = MockApi(json_reply({"data": [{"contact_id": "ct_1"}]}))
    events: list[SendEventOptions] = [
        {"event": "signed_up", "email": "jane@acme.dev", "user_id": "usr_1"},
        {"event": "paid", "user_id": "usr_1", "occurred_at": "2026-11-14T09:30:00Z"},
    ]

    result = api.client().events.batch(events)

    assert result == {"data": [{"contact_id": "ct_1"}]}
    assert api.routes() == ["POST https://api.test/v1/events/batch"]
    assert json.loads(api.requests[0].content) == events
