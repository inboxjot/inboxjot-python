from helpers import MockApi, check_routes, json_reply

from inboxjot.types import Domain, DomainPage

BASE = "https://api.test/v1/domains"


def test_maps_each_method_to_its_route() -> None:
    check_routes(
        [
            (lambda i: i.domains.list({"per_page": 5}), f"GET {BASE}?per_page=5"),
            (lambda i: i.domains.create({"name": "acme.dev"}), f"POST {BASE}"),
            (lambda i: i.domains.get("dom_1"), f"GET {BASE}/dom_1"),
            (lambda i: i.domains.delete("dom_1"), f"DELETE {BASE}/dom_1"),
            (lambda i: i.domains.verify("dom_1"), f"POST {BASE}/dom_1/verify"),
        ]
    )


def test_decodes_domains() -> None:
    domain: Domain = {
        "id": "dom_1",
        "name": "acme.dev",
        "mail_from_domain": "send.acme.dev",
        "status": "pending",
        "records": [
            {
                "kind": "dkim",
                "type": "TXT",
                "name": "ibx._domainkey.acme.dev",
                "value": "p=abc",
                "status": "pending",
            },
            {
                "kind": "return_path",
                "type": "MX",
                "name": "send.acme.dev",
                "value": "feedback.example.com",
                "priority": 10,
                "status": "verified",
            },
        ],
        "region": "us-east-1",
        "tls_policy": "opportunistic",
        "receiving_enabled": False,
        "receiving_target": "",
        "receiving_status": "not_started",
        "receiving_found_mx": None,
        "receiving_checked_at": None,
        "receiving_verified_at": None,
        "open_tracking": False,
        "click_tracking": False,
        "tracking_domain": None,
        "tracking_status": "not_started",
        "tracking_records": [],
        "tracking_verified_at": None,
        "mailing_address": None,
        "verified_at": None,
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
        "sent_last_30_days": 0,
        "bounced_last_30_days": 0,
        "is_default": False,
        "receiving": {"host": "acme.dev", "mx": "mx.example.com", "shared_address": None},
        "warmup": {
            "enabled": False,
            "started_on": None,
            "day": None,
            "limit": None,
            "next_limit": None,
            "sent_today": 0,
            "full_volume_on": None,
        },
    }
    page: DomainPage = {
        "data": [
            {
                "id": "dom_1",
                "name": "acme.dev",
                "status": "verified",
                "pending_record_kinds": [],
                "region": "us-east-1",
                "is_default": True,
                "open_tracking": False,
                "click_tracking": False,
                "sent_last_30_days": 0,
                "verified_at": None,
                "created_at": "2026-10-20T09:00:00Z",
            }
        ],
        "next_cursor": None,
        "prev_cursor": None,
    }
    unknown = {**domain, "status": "melted", "tracking_status": "melted"}
    api = MockApi(json_reply(unknown), json_reply(page))
    inboxjot = api.client()

    result = inboxjot.domains.get("dom_1")

    assert result == unknown
    assert "priority" not in result["records"][0]
    assert inboxjot.domains.list() == page
