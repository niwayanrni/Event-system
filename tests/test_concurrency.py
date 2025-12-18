# tests/test_concurrency.py
import asyncio
import pytest

@pytest.mark.asyncio
async def test_concurrent_publish(client):
    event = {
        "topic": "race",
        "event_id": "race-1",
        "timestamp": "2025-12-18T10:00:00Z",
        "source": "pytest",
        "payload": {}
    }

    await asyncio.gather(
        *[client.post("/publish", json=event) for _ in range(10)]
    )

    stats = (await client.get("/stats")).json()
    assert stats["unique_processed"] == 1
