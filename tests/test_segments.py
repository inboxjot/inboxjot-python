from helpers import MockApi, check_routes, json_reply, read_body

from inboxjot.types import Segment, SegmentMemberPage, SegmentPage

BASE = "https://api.test/v1/segments"


def test_maps_each_method_to_its_route() -> None:
    members = {"contact_ids": ["ct_1"]}

    check_routes(
        [
            (lambda i: i.segments.list({"type": "static"}), f"GET {BASE}?type=static"),
            (lambda i: i.segments.create({"name": "Beta", "type": "static"}), f"POST {BASE}"),
            (lambda i: i.segments.get("sg_1"), f"GET {BASE}/sg_1"),
            (lambda i: i.segments.update("sg_1", {"name": "Alpha"}), f"PATCH {BASE}/sg_1"),
            (lambda i: i.segments.delete("sg_1"), f"DELETE {BASE}/sg_1"),
            (
                lambda i: i.segments.list_members("sg_1", {"query": "riti"}),
                f"GET {BASE}/sg_1/members?query=riti",
            ),
            (lambda i: i.segments.add_members("sg_1", members), f"POST {BASE}/sg_1/members"),
            (lambda i: i.segments.remove_members("sg_1", members), f"DELETE {BASE}/sg_1/members"),
        ]
    )


def test_sends_remove_members_as_a_delete_with_a_json_body() -> None:
    api = MockApi(json_reply({"removed": 1}))

    result = api.client().segments.remove_members("sg_1", {"contact_ids": ["ct_1"]})

    request = api.requests[0]
    assert result == {"removed": 1}
    assert request.method == "DELETE"
    assert request.headers["Content-Type"] == "application/json"
    assert read_body(request) == {"contact_ids": ["ct_1"]}


def test_decodes_segments() -> None:
    segment: Segment = {
        "id": "sg_1",
        "name": "Beta",
        "description": None,
        "type": "dynamic",
        "conditions": {
            "match": "all",
            "rules": [
                {"field": "email", "operator": "is_set"},
                {"field": "opened", "operator": "at_least", "value": {"count": 2, "days": 30}},
            ],
        },
        "contact_count": None,
        "counted_at": None,
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    page: SegmentPage = {
        "data": [
            {
                "id": "sg_1",
                "name": "Beta",
                "description": None,
                "type": "static",
                "contact_count": 0,
                "counted_at": None,
                "created_at": "2026-10-20T09:00:00Z",
                "updated_at": "2026-10-20T09:00:00Z",
            }
        ],
        "total": 1,
        "next_cursor": None,
        "prev_cursor": None,
    }
    members: SegmentMemberPage = {
        "data": [
            {
                "id": "ct_1",
                "email": "riti@example.com",
                "first_name": None,
                "last_name": None,
                "status": "subscribed",
                "joined_at": "2026-10-20T09:00:00Z",
            }
        ],
        "next_cursor": None,
        "prev_cursor": None,
    }
    unknown = {**segment, "type": "smart"}
    api = MockApi(json_reply(unknown), json_reply(page), json_reply(members))
    inboxjot = api.client()

    assert inboxjot.segments.get("sg_1") == unknown
    assert inboxjot.segments.list() == page
    assert inboxjot.segments.list_members("sg_1") == members
