from helpers import MockApi, check_routes, json_reply

from inboxjot.types import Brand, BrandPage

BASE = "https://api.test/v1/brands"


def test_maps_each_method_to_its_route() -> None:
    check_routes(
        [
            (lambda i: i.brands.list({"after": "brd_0"}), f"GET {BASE}?after=brd_0"),
            (lambda i: i.brands.create({"name": "Acme Labs"}), f"POST {BASE}"),
            (lambda i: i.brands.get("brd_1"), f"GET {BASE}/brd_1"),
            (lambda i: i.brands.update("brd_1", {"name": "Acme Studio"}), f"PATCH {BASE}/brd_1"),
            (lambda i: i.brands.delete("brd_1"), f"DELETE {BASE}/brd_1"),
        ]
    )


def test_decodes_brands() -> None:
    brand: Brand = {
        "id": "brd_1",
        "name": "Acme",
        "slug": "acme",
        "logo_url": None,
        "is_default": True,
        "default_topic_id": "tp_1",
        "topic_count": 3,
        "created_at": "2026-10-20T09:00:00Z",
        "updated_at": "2026-10-20T09:00:00Z",
    }
    page: BrandPage = {"data": [brand], "next_cursor": None, "prev_cursor": None}
    api = MockApi(json_reply(brand), json_reply(page))
    inboxjot = api.client()

    assert inboxjot.brands.get("brd_1") == brand
    assert inboxjot.brands.list() == page
