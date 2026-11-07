import asyncio
import json

from helpers import MockApi, json_reply

from inboxjot.types import SendEventOptions


def test_maps_send_to_its_route() -> None:
    api = MockApi(json_reply({"contact_id": "ct_1"}))
    event: SendEventOptions = {
        "name": "signed_up",
        "email": "jane@acme.dev",
        "data": {"plan": "pro"},
    }

    result = api.client().events.send(event)

    assert result == {"contact_id": "ct_1"}
    assert api.routes() == ["POST https://api.test/v1/events"]
    assert json.loads(api.requests[0].content) == event


def test_async_client_maps_send_to_its_route() -> None:
    api = MockApi(json_reply({"contact_id": "ct_1"}))

    async def run() -> None:
        async with api.async_client() as inboxjot:
            await inboxjot.events.send({"name": "signed_up", "email": "jane@acme.dev"})

    asyncio.run(run())

    assert api.routes() == ["POST https://api.test/v1/events"]
