![Inboxjot](https://inboxjot.com/og.png)

<p align="center">The official Python SDK for the Inboxjot email API. <br />Email for builders and their agents.</p>

<p align="center">
  <a href="https://pypi.org/project/inboxjot/"><img src="https://inboxjot.com/badges/pypi.svg?v=2" alt="PyPI" height="24" /></a>
  <a href="./LICENSE"><img src="https://inboxjot.com/badges/license.svg?v=2" alt="License" height="24" /></a>
  <a href="https://inboxjot.com/docs"><img src="https://inboxjot.com/badges/docs.svg?v=2" alt="Docs" height="24" /></a>
</p>

Send email, manage contacts, campaigns, templates and domains, and verify webhooks from your Python app. It needs Python 3.10+ and has one runtime dependency, [`httpx`](https://www.python-httpx.org). It has a sync client, `Inboxjot`, and an async client, `AsyncInboxjot`, with the same methods.

## Install

```sh
pip install inboxjot
```

## Usage

```python
from inboxjot import Inboxjot

inboxjot = Inboxjot(api_key="ibx_...")

email = inboxjot.emails.send(
    {
        "from": "Acme <hi@acme.dev>",
        "to": "jane@example.com",
        "subject": "Welcome",
        "html": "<p>Hi Jane</p>",
    }
)
print(email["id"])
```

If you do not give an API key, the client reads `INBOXJOT_API_KEY` from the environment.

```python
inboxjot = Inboxjot(
    base_url="https://api.inboxjot.com",
    timeout=60.0,
    max_retries=2,
    http_client=httpx.Client(),
)
```

The client keeps a connection pool. Use it as a context manager, or call `inboxjot.close()` when you are done.

The async client takes the same options, and an `httpx.AsyncClient` as `http_client`:

```python
from inboxjot import AsyncInboxjot

async with AsyncInboxjot() as inboxjot:
    email = await inboxjot.emails.get("em_...")
```

### Emails

```python
inboxjot.emails.send(
    {
        "from": sender,
        "to": ["a@example.com"],
        "subject": subject,
        "text": text,
        "scheduled_at": "2026-10-20T09:00:00Z",
    }
)
inboxjot.emails.batch(
    [
        {"from": sender, "to": "a@example.com", "subject": subject, "html": html},
        {"from": sender, "to": "b@example.com", "subject": subject, "html": html},
    ]
)
inboxjot.emails.list({"status": "delivered", "per_page": 20})
inboxjot.emails.get("em_...")
inboxjot.emails.update("em_...", {"scheduled_at": "2026-10-21T09:00:00Z"})
inboxjot.emails.cancel("em_...")
inboxjot.emails.list_attachments("em_...")
inboxjot.emails.get_attachment("em_...", "att_...")
```

### Contacts and events

```python
contact = inboxjot.contacts.create({"email": "jane@example.com", "first_name": "Jane"})
inboxjot.contacts.list({"status": "subscribed", "per_page": 50})
inboxjot.contacts.get(contact["id"])
inboxjot.contacts.get("jane@example.com")
inboxjot.contacts.update(contact["id"], {"topics": [{"id": "tp_...", "status": "unsubscribed"}]})
inboxjot.contacts.delete(contact["id"])
inboxjot.contacts.erase({"email": "jane@example.com"})

inboxjot.events.send({"name": "signed_up", "email": "jane@example.com", "data": {"plan": "pro"}})
```

`contacts.remove` deletes the contact. `contacts.erase` queues a privacy erasure of the address, its emails, events and logs.

### Campaigns

```python
campaign = inboxjot.campaigns.create({"name": "October", "subject": "News"})
inboxjot.campaigns.list({"status": "draft,scheduled", "per_page": 20})
inboxjot.campaigns.get(campaign["id"])
inboxjot.campaigns.update(campaign["id"], {"subject": "October news"})
inboxjot.campaigns.send_test(campaign["id"], {"to": ["jane@example.com"]})
inboxjot.campaigns.send(campaign["id"])
inboxjot.campaigns.send(campaign["id"], {"scheduled_at": "2026-10-20T09:00:00Z"})
inboxjot.campaigns.cancel(campaign["id"])
inboxjot.campaigns.delete(campaign["id"])
```

### Templates

```python
template = inboxjot.templates.create({"name": "Welcome", "starter_id": "welcome"})
inboxjot.templates.list({"sort": "name"})
inboxjot.templates.get(template["id"])
inboxjot.templates.update(template["id"], {"subject": "Welcome"})
inboxjot.templates.publish(template["id"])
inboxjot.templates.delete(template["id"])
```

### Versions

Campaigns and templates have the same version methods. `update_version` always takes `name`, and `None` clears it.

```python
version = inboxjot.templates.create_version(template["id"], {"name": "Launch"})
inboxjot.templates.list_versions(template["id"], {"filter": "saved"})
inboxjot.templates.get_version(template["id"], version["id"])
inboxjot.templates.update_version(template["id"], version["id"], {"name": None})
inboxjot.templates.restore_version(template["id"], version["id"])
```

### Domains

```python
domain = inboxjot.domains.create({"name": "acme.dev"})
inboxjot.domains.list()
inboxjot.domains.get(domain["id"])
inboxjot.domains.verify(domain["id"])
inboxjot.domains.delete(domain["id"])
```

### Images

An image that is already online goes straight into email content as `<img src="https://…">`. To host a file on Inboxjot, upload it. The SDK accepts PNG, JPEG and GIF files.

```python
with open("logo.png", "rb") as file:
    image = inboxjot.images.upload({"file": file.read(), "file_name": "logo.png"})

inboxjot.images.list({"type": "png"})
inboxjot.images.get(image["id"])
inboxjot.images.delete(image["id"])
```

### Segments and topics

```python
segment = inboxjot.segments.create({"name": "Beta", "type": "static"})
inboxjot.segments.list({"type": "static"})
inboxjot.segments.get(segment["id"])
inboxjot.segments.update(segment["id"], {"name": "Early Access"})
inboxjot.segments.add_members(segment["id"], {"contact_ids": ["ct_..."]})
inboxjot.segments.list_members(segment["id"], {"query": "jane"})
inboxjot.segments.remove_members(segment["id"], {"contact_ids": ["ct_..."]})
inboxjot.segments.delete(segment["id"])

topic = inboxjot.topics.create({"name": "Product News"})
inboxjot.topics.list()
inboxjot.topics.get(topic["id"])
inboxjot.topics.update(topic["id"], {"visibility": "private"})
inboxjot.topics.delete(topic["id"])
```

### Pagination

Lists page with a cursor. Pass `next_cursor` back as `after`. It is `None` on the last page, and the client leaves a `None` cursor out of the request.

```python
after = None
while True:
    page = inboxjot.contacts.list({"per_page": 100, "after": after})
    after = page["next_cursor"]
    if after is None:
        break
```

### Idempotency and retries

Every method takes request options as keyword arguments:

```python
inboxjot.emails.send(email, idempotency_key=f"welcome-{user.id}")
```

| Option            | Use                                         |
| ----------------- | ------------------------------------------- |
| `idempotency_key` | Sends the `Idempotency-Key` header.         |
| `timeout`         | Overrides the client timeout, in seconds.   |
| `max_retries`     | Overrides the client retry count.           |

The client retries with exponential backoff, and it honors `Retry-After`. A `Retry-After` over 60 seconds raises the error with no retry:

- `429` and `409 concurrent_idempotent_requests` always retry. The API did not run these requests.
- `5xx`, timeouts and network errors retry only when the retry is safe: a `GET` or `DELETE`, or a request with an `idempotency_key`.

An email send without a key is never retried after a network error, because that can send the email twice. Give a key to make it safe.

### Errors

A failed request raises. An API error is an `InboxjotError` with the fields of the API error body. A network error or timeout is an `InboxjotConnectionError`.

```python
from inboxjot import InboxjotError

try:
    inboxjot.emails.get("em_...")
except InboxjotError as error:
    if error.name == "not_found":
        ...  # error.status, error.message, error.errors, error.request_id, error.headers
```

The SDK raises instead of returning `(data, error)`. A result tuple makes you check every call, and an unchecked error turns into `None` data later in the code. A raised error stops the flow at the failed call, and it works with `asyncio.gather` and with the retry loop. `error.name` is typed as a `Literal` of the API error names.

### Webhooks

```python
webhook = inboxjot.webhooks.create(
    {"name": "Production", "url": "https://acme.dev/hook", "events": ["email.bounced"]}
)
print(webhook["secret"])
inboxjot.webhooks.list()
inboxjot.webhooks.get(webhook["id"])
inboxjot.webhooks.update(webhook["id"], {"status": "disabled"})
inboxjot.webhooks.delete(webhook["id"])
```

Inboxjot signs webhooks with the [Standard Webhooks](https://www.standardwebhooks.com) spec. Verify the raw request body before you parse it:

```python
import os

from fastapi import FastAPI, Request, Response
from inboxjot import verify_webhook

app = FastAPI()


@app.post("/webhooks/inboxjot")
async def handle(request: Request):
    event = verify_webhook(
        payload=await request.body(),
        headers=request.headers,
        secret=os.environ["INBOXJOT_WEBHOOK_SECRET"],
    )
    if event["type"] == "email.bounced":
        print(event["data"]["email_id"], event["data"]["bounce"]["type"])
    elif event["type"] == "contact.created":
        print(event["data"]["contact_id"])
    return Response(status_code=204)
```

`inboxjot.webhooks.verify` is the same function. The payload can be `str` or `bytes`, and the headers can be any mapping, such as a `dict` or a framework's headers object. A bad signature, a missing header or a timestamp more than 5 minutes off raises a `WebhookVerificationError`.

## Types

`inboxjot.types` has a `TypedDict` or `Literal` for each schema in the Inboxjot OpenAPI spec, with the names the TypeScript SDK uses (`SendEmailOptions`, `Email`, `Contact`, `WebhookEvent` and the others). Request and response bodies are plain dicts with the API's own keys, so `scheduled_at` stays `scheduled_at`. `WebhookEvent` is a union that a type checker narrows on `event["type"]`.

```python
from inboxjot.types import Email, SendEmailOptions

email: SendEmailOptions = {"to": "jane@example.com", "subject": "Hi", "text": "Hi"}
```

The client does not validate responses, so a new enum value or field reaches your code as is.

If a type is wrong, fix the spec in the API and update `src/inboxjot/types.py` to match.

## Layout

```
src/inboxjot/_client.py     Inboxjot, AsyncInboxjot and request(): auth, idempotency, timeout, retries
src/inboxjot/_emails.py     emails.list, send, batch, get, update, cancel, list_attachments, get_attachment
src/inboxjot/_contacts.py   contacts.list, create, get, update, remove, erase
src/inboxjot/_events.py     events.send
src/inboxjot/_campaigns.py  campaigns.list, create, get, update, remove, send, cancel, send_test, versions
src/inboxjot/_templates.py  templates.list, create, get, update, remove, publish, versions
src/inboxjot/_domains.py    domains.list, create, get, remove, verify
src/inboxjot/_images.py     images.list, upload, get, remove
src/inboxjot/_segments.py   segments.list, create, get, update, remove, list_members, add_members, remove_members
src/inboxjot/_topics.py     topics.list, create, get, update, remove
src/inboxjot/_webhooks.py   webhooks.list, create, get, update, remove, verify, verify_webhook
src/inboxjot/_errors.py     InboxjotError, InboxjotConnectionError, WebhookVerificationError
src/inboxjot/types.py       the request and response types
```

## Development

```sh
uv sync
uv run pytest
uv run ruff check
uv run ruff format
uv run pyright
uv build
```

To release, run `uv version --bump patch` (or `minor`), commit `chore: release vX.Y.Z`, then tag `vX.Y.Z` and push the tag. The release workflow checks, builds and publishes to PyPI.
