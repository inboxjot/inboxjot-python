import asyncio
import time

import pytest


@pytest.fixture(autouse=True)
def sleeps(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    delays: list[float] = []

    async def async_sleep(delay: float) -> None:
        delays.append(delay)

    monkeypatch.setattr(time, "sleep", delays.append)
    monkeypatch.setattr(asyncio, "sleep", async_sleep)

    return delays
