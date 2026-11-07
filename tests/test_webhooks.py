import base64
import hashlib
import hmac
import time

import httpx
import pytest
from helpers import MockApi, check_routes, json_reply, read_body

from inboxjot import AsyncInboxjot, Inboxjot, WebhookVerificationError, verify_webhook
from inboxjot.types import UpdateWebhookResponse, Webhook, WebhookEvent

SECRET = "whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaSw"
OTHER_SECRET = "whsec_3kTmPqZ8vXw2RbN7cYhJ4dLsF9gA6eUu"
ID = "msg_p5jXN8AQM9LWM0D4loKWxJek"
TIMESTAMP = 1_614_265_330
PAYLOAD = '{"test": 2432232314}'
SIGNATURE = "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE="


def create_headers(
    signature: str = SIGNATURE,
    timestamp: object = TIMESTAMP,
    webhook_id: str = ID,
) -> dict[str, str]:
    return {
        "webhook-id": webhook_id,
        "webhook-timestamp": str(timestamp),
        "webhook-signature": signature,
    }


def sign(secret: str, webhook_id: str, timestamp: int, payload: str) -> str:
    key = base64.b64decode(secret.removeprefix("whsec_"))
    content = f"{webhook_id}.{timestamp}.{payload}".encode()
    mac = hmac.new(key, content, hashlib.sha256).digest()

    return f"v1,{base64.b64encode(mac).decode()}"


@pytest.fixture
def now(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(time, "time", lambda: float(TIMESTAMP))


def test_verifies_the_standard_webhooks_test_vector(now: None) -> None:
    event = verify_webhook(payload=PAYLOAD, headers=create_headers(), secret=SECRET)

    assert event == {"test": 2432232314}


def test_matches_the_signature_the_api_produces() -> None:
    assert sign(SECRET, ID, TIMESTAMP, PAYLOAD) == SIGNATURE


def test_accepts_httpx_headers_bytes_and_several_signatures(now: None) -> None:
    headers = httpx.Headers(create_headers(f"v1,bm90IGl0 v2,abc {SIGNATURE}"))

    event = Inboxjot(api_key="ibx_test").webhooks.verify(
        payload=PAYLOAD.encode(), headers=headers, secret=SECRET
    )

    assert event == {"test": 2432232314}


def test_reads_headers_in_any_case(now: None) -> None:
    headers = {key.title(): value for key, value in create_headers().items()}

    assert verify_webhook(payload=PAYLOAD, headers=headers, secret=SECRET) == {"test": 2432232314}


def test_verifies_a_freshly_signed_payload() -> None:
    timestamp = int(time.time())
    signature = sign(OTHER_SECRET, "evt_1", timestamp, "{}")
    headers = create_headers(signature, timestamp, "evt_1")

    assert verify_webhook(payload="{}", headers=headers, secret=OTHER_SECRET) == {}


@pytest.mark.parametrize(
    ("payload", "headers", "secret", "message"),
    [
        ('{"test": 1}', create_headers(), SECRET, "No matching signature found"),
        (PAYLOAD, create_headers(webhook_id="msg_other"), SECRET, "No matching signature found"),
        (PAYLOAD, create_headers(f"v1a,{SIGNATURE[3:]}"), SECRET, "No matching signature found"),
        (PAYLOAD, create_headers(), OTHER_SECRET, "No matching signature found"),
        (PAYLOAD, create_headers(timestamp=TIMESTAMP - 301), SECRET, "outside the tolerance"),
        (PAYLOAD, create_headers(timestamp=TIMESTAMP + 301), SECRET, "outside the tolerance"),
        (PAYLOAD, create_headers(timestamp="soon"), SECRET, "Invalid webhook timestamp"),
        (PAYLOAD, create_headers(timestamp="9" * 400), SECRET, "outside the tolerance"),
        (PAYLOAD, create_headers(timestamp="-" + "9" * 400), SECRET, "outside the tolerance"),
        (PAYLOAD, create_headers(timestamp="9" * 5000), SECRET, "Invalid webhook timestamp"),
        (PAYLOAD, create_headers("v1,caf\u00e9"), SECRET, "No matching signature found"),
        (PAYLOAD, create_headers(), "whsec_", "Invalid webhook secret"),
        (PAYLOAD, create_headers(), "whsec_caf\u00e9", "Invalid webhook secret"),
        (PAYLOAD, create_headers(), "whsec_not base64", "Invalid webhook secret"),
        (PAYLOAD, {}, SECRET, "Missing webhook headers"),
    ],
)
def test_rejects_bad_webhooks(
    now: None,
    payload: str,
    headers: dict[str, str],
    secret: str,
    message: str,
) -> None:
    with pytest.raises(WebhookVerificationError, match=message):
        verify_webhook(payload=payload, headers=headers, secret=secret)


def test_narrows_the_event_data_by_type() -> None:
    def read_detail(event: WebhookEvent) -> str | None:
        if event["type"] == "email.bounced":
            return event["data"]["bounce"]["message"]
        if event["type"] == "email.failed":
            return event["data"]["reason"]
        if event["type"] == "contact.created":
            return event["data"]["contact_id"]

        return None

    failed_event: WebhookEvent = {
        "id": "evt_1",
        "created_at": "2026-10-17T00:00:00Z",
        "type": "email.failed",
        "data": {
            "email_id": "em_1",
            "to": ["a@b.c"],
            "from": "f@b.c",
            "subject": "S",
            "reason": "Bad",
        },
    }

    assert read_detail(failed_event) == "Bad"


def test_async_client_verifies_without_awaiting(now: None) -> None:
    event = AsyncInboxjot(api_key="ibx_test").webhooks.verify(
        payload=PAYLOAD, headers=create_headers(), secret=SECRET
    )

    assert event == {"test": 2432232314}


def test_maps_each_endpoint_method_to_its_route() -> None:
    body = {"name": "Prod", "url": "https://acme.dev/hook", "events": ["email.sent"]}

    check_routes(
        [
            (
                lambda i: i.webhooks.list({"per_page": 10}),
                "GET https://api.test/v1/webhooks?per_page=10",
            ),
            (lambda i: i.webhooks.create(body), "POST https://api.test/v1/webhooks"),
            (lambda i: i.webhooks.get("wh_1"), "GET https://api.test/v1/webhooks/wh_1"),
            (
                lambda i: i.webhooks.update("wh_1", {"status": "disabled"}),
                "PATCH https://api.test/v1/webhooks/wh_1",
            ),
            (lambda i: i.webhooks.delete("wh_1"), "DELETE https://api.test/v1/webhooks/wh_1"),
        ]
    )


def test_decodes_webhook_endpoints() -> None:
    endpoint: UpdateWebhookResponse = {
        "id": "wh_1",
        "name": "Prod",
        "url": "https://acme.dev/hook",
        "events": ["email.sent"],
        "status": "enabled",
        "disabled_reason": None,
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    detail: Webhook = {
        **endpoint,
        "deliveries_24h": 0,
        "success_rate": None,
        "avg_duration_ms": None,
        "retrying": 0,
        "recent_deliveries": [
            {
                "delivery_id": "del_1",
                "event_id": "evt_1",
                "event_type": "email.sent",
                "endpoint_id": "wh_1",
                "email_id": "em_1",
                "status": 200,
                "attempt": 1,
                "duration_ms": 12,
                "created_at": "2026-10-20T09:00:00Z",
                "last_attempt_at": "2026-10-20T09:00:00Z",
                "next_attempt_at": None,
            }
        ],
    }
    unknown = {**detail, "status": "paused", "events": ["email.teleported"]}
    created = {**endpoint, "secret": "whsec_abc"}
    api = MockApi(json_reply(unknown), json_reply(created, 201))
    inboxjot = api.client()

    assert inboxjot.webhooks.get("wh_1") == unknown
    assert (
        inboxjot.webhooks.create({"name": "Prod", "url": "https://a.b", "events": []})["secret"]
        == "whsec_abc"
    )
    assert read_body(api.requests[1])["events"] == []


def test_verifies_an_unknown_event_type() -> None:
    timestamp = int(time.time())
    payload = '{"id":"evt_1","type":"email.teleported","created_at":"x","data":{}}'
    headers = create_headers(sign(SECRET, ID, timestamp, payload), timestamp)

    assert (
        verify_webhook(payload=payload, headers=headers, secret=SECRET)["type"]
        == "email.teleported"
    )
