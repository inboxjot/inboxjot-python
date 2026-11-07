from helpers import MockApi, check_routes, json_reply, read_body

from inboxjot.types import Campaign, CampaignPage, CampaignVersionDetail, CampaignVersionPage

BASE = "https://api.test/v1/campaigns"


def test_maps_each_method_to_its_route() -> None:
    check_routes(
        [
            (lambda i: i.campaigns.list({"per_page": 10}), f"GET {BASE}?per_page=10"),
            (lambda i: i.campaigns.create({"name": "October"}), f"POST {BASE}"),
            (lambda i: i.campaigns.get("cmp_1"), f"GET {BASE}/cmp_1"),
            (lambda i: i.campaigns.update("cmp_1", {"subject": "Hi"}), f"PATCH {BASE}/cmp_1"),
            (lambda i: i.campaigns.delete("cmp_1"), f"DELETE {BASE}/cmp_1"),
            (lambda i: i.campaigns.send("cmp_1"), f"POST {BASE}/cmp_1/send"),
            (lambda i: i.campaigns.cancel("cmp_1"), f"POST {BASE}/cmp_1/cancel"),
            (
                lambda i: i.campaigns.send_test("cmp_1", {"to": ["a@b.c"]}),
                f"POST {BASE}/cmp_1/test",
            ),
            (
                lambda i: i.campaigns.list_versions("cmp_1", {"filter": "saved"}),
                f"GET {BASE}/cmp_1/versions?filter=saved",
            ),
            (
                lambda i: i.campaigns.create_version("cmp_1", {"name": "v1"}),
                f"POST {BASE}/cmp_1/versions",
            ),
            (
                lambda i: i.campaigns.get_version("cmp_1", "ver 1"),
                f"GET {BASE}/cmp_1/versions/ver%201",
            ),
            (
                lambda i: i.campaigns.update_version("cmp_1", "ver_1", {"name": None}),
                f"PATCH {BASE}/cmp_1/versions/ver_1",
            ),
            (
                lambda i: i.campaigns.restore_version("cmp_1", "ver_1"),
                f"POST {BASE}/cmp_1/versions/ver_1/restore",
            ),
        ]
    )


def test_sends_an_empty_body_or_the_given_schedule() -> None:
    api = MockApi(json_reply({}, 202), json_reply({}, 202))
    inboxjot = api.client()

    inboxjot.campaigns.send("cmp_1")
    inboxjot.campaigns.send("cmp_1", {"scheduled_at": "2026-10-20T09:00:00Z"})

    assert read_body(api.requests[0]) == {}
    assert read_body(api.requests[1]) == {"scheduled_at": "2026-10-20T09:00:00Z"}


def test_sends_a_null_version_name() -> None:
    api = MockApi(json_reply({}))

    api.client().campaigns.update_version("cmp_1", "ver_1", {"name": None})

    assert read_body(api.requests[0]) == {"name": None}


def test_sends_a_comma_separated_status() -> None:
    api = MockApi(json_reply({}))

    api.client().campaigns.list({"status": "draft,sent"})

    assert api.requests[0].url.params["status"] == "draft,sent"


def test_decodes_campaigns() -> None:
    campaign: Campaign = {
        "id": "cmp_1",
        "name": "October",
        "status": "draft",
        "from": "Acme <hi@acme.dev>",
        "reply_to": None,
        "subject": "Hi",
        "preheader": "",
        "html": None,
        "text": None,
        "template_id": None,
        "template": None,
        "include_segment_ids": ["sg_1"],
        "include_segments": [{"id": "sg_1", "name": "Beta"}],
        "exclude_segment_ids": [],
        "exclude_segments": [],
        "topic_id": "tp_1",
        "topic": None,
        "audience_count": None,
        "queued_count": 0,
        "skipped_count": 0,
        "paused_reason": None,
        "failure_reason": None,
        "scheduled_at": None,
        "started_at": None,
        "completed_at": None,
        "warmup_next_limit": None,
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    page: CampaignPage = {
        "data": [
            {
                "id": "cmp_1",
                "name": "October",
                "status": "paused",
                "subject": "Hi",
                "include_segments": [],
                "exclude_segments": [],
                "topic": None,
                "audience_count": None,
                "queued_count": 0,
                "skipped_count": 0,
                "paused_reason": "warmup",
                "scheduled_at": None,
                "started_at": None,
                "completed_at": None,
                "created_at": "2026-10-20T09:00:00Z",
                "updated_at": "2026-10-20T09:00:00Z",
                "stats": None,
            }
        ],
        "next_cursor": None,
        "prev_cursor": None,
    }
    unknown = {**campaign, "status": "archived", "paused_reason": "moon_phase"}
    api = MockApi(json_reply(unknown), json_reply(page))
    inboxjot = api.client()

    assert inboxjot.campaigns.get("cmp_1") == unknown
    assert inboxjot.campaigns.list() == page


def test_decodes_campaign_versions() -> None:
    page: CampaignVersionPage = {
        "data": [
            {
                "id": "ver_1",
                "reason": "manual",
                "name": None,
                "editors": [{"kind": "api", "id": "key_1", "name": "CI"}],
                "created_at": "2026-10-20T09:00:00Z",
            }
        ],
        "total": 1,
        "next_cursor": None,
        "prev_cursor": None,
    }
    detail: CampaignVersionDetail = {
        **page["data"][0],
        "from": "Acme <hi@acme.dev>",
        "reply_to": None,
        "subject": "Hi",
        "preheader": "",
        "html": "<p>Hi</p>",
        "text": "Hi",
        "content": {"type": "doc"},
    }
    unknown = {**detail, "reason": "time_travel"}
    api = MockApi(json_reply(page), json_reply(unknown))
    inboxjot = api.client()

    assert inboxjot.campaigns.list_versions("cmp_1") == page
    assert inboxjot.campaigns.get_version("cmp_1", "ver_1") == unknown
