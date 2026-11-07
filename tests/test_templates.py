from helpers import MockApi, check_routes, json_reply, read_body

from inboxjot.types import Template, TemplatePage

BASE = "https://api.test/v1/templates"


def test_maps_each_method_to_its_route() -> None:
    check_routes(
        [
            (lambda i: i.templates.list({"sort": "name"}), f"GET {BASE}?sort=name"),
            (lambda i: i.templates.create({"name": "Welcome"}), f"POST {BASE}"),
            (lambda i: i.templates.get("tpl_1"), f"GET {BASE}/tpl_1"),
            (lambda i: i.templates.update("tpl_1", {"subject": "Hi"}), f"PATCH {BASE}/tpl_1"),
            (lambda i: i.templates.delete("tpl_1"), f"DELETE {BASE}/tpl_1"),
            (lambda i: i.templates.publish("tpl_1"), f"POST {BASE}/tpl_1/publish"),
            (
                lambda i: i.templates.list_versions("tpl_1", {"filter": "all"}),
                f"GET {BASE}/tpl_1/versions?filter=all",
            ),
            (
                lambda i: i.templates.create_version("tpl_1", {"name": "v1"}),
                f"POST {BASE}/tpl_1/versions",
            ),
            (
                lambda i: i.templates.get_version("tpl_1", "ver_1"),
                f"GET {BASE}/tpl_1/versions/ver_1",
            ),
            (
                lambda i: i.templates.update_version("tpl_1", "ver_1", {"name": None}),
                f"PATCH {BASE}/tpl_1/versions/ver_1",
            ),
            (
                lambda i: i.templates.restore_version("tpl_1", "ver_1"),
                f"POST {BASE}/tpl_1/versions/ver_1/restore",
            ),
        ]
    )


def test_sends_a_null_version_name() -> None:
    api = MockApi(json_reply({}))

    api.client().templates.update_version("tpl_1", "ver_1", {"name": None})

    assert read_body(api.requests[0]) == {"name": None}


def test_decodes_templates() -> None:
    template: Template = {
        "id": "tpl_1",
        "name": "Welcome",
        "from": "Acme <hi@acme.dev>",
        "reply_to": None,
        "subject": "Hi",
        "preheader": "",
        "html": "<p>Hi</p>",
        "text": "Hi",
        "published_version_id": None,
        "has_unpublished_changes": True,
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    page: TemplatePage = {
        "data": [
            {
                "id": "tpl_1",
                "name": "Welcome",
                "from": "Acme <hi@acme.dev>",
                "subject": "Hi",
                "preheader": "",
                "stats": {"sent": 0, "opened": 0, "clicked": 0},
                "used_in": {"count": 0, "first": None},
                "created_at": "2026-10-20T09:00:00Z",
                "updated_at": "2026-10-20T09:00:00Z",
            }
        ],
        "next_cursor": None,
        "prev_cursor": None,
    }
    api = MockApi(json_reply(template), json_reply(page))
    inboxjot = api.client()

    assert inboxjot.templates.get("tpl_1") == template
    assert inboxjot.templates.list() == page
