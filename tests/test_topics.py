from helpers import MockApi, check_routes, json_reply

from inboxjot.types import Topic, TopicPage

BASE = "https://api.test/v1/topics"


def test_maps_each_method_to_its_route() -> None:
    check_routes(
        [
            (lambda i: i.topics.list({"after": "tp_0"}), f"GET {BASE}?after=tp_0"),
            (lambda i: i.topics.create({"name": "News"}), f"POST {BASE}"),
            (lambda i: i.topics.get("tp_1"), f"GET {BASE}/tp_1"),
            (lambda i: i.topics.update("tp_1", {"visibility": "private"}), f"PATCH {BASE}/tp_1"),
            (lambda i: i.topics.delete("tp_1"), f"DELETE {BASE}/tp_1"),
        ]
    )


def test_decodes_topics() -> None:
    topic: Topic = {
        "id": "tp_1",
        "name": "News",
        "description": None,
        "default_subscribed": True,
        "visibility": "public",
        "double_opt_in": False,
        "form_enabled": False,
        "sender_name": None,
        "sender_email": None,
        "redirect_url": None,
        "is_default": True,
        "counts": {"subscribed": 1, "pending": 0, "unsubscribed": 0},
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    page: TopicPage = {"data": [topic], "next_cursor": None, "prev_cursor": None}
    unknown = {**topic, "visibility": "secret"}
    api = MockApi(json_reply(unknown), json_reply(page))
    inboxjot = api.client()

    assert inboxjot.topics.get("tp_1") == unknown
    assert inboxjot.topics.list() == page
