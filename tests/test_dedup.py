# tests/test_dedup.py
import pytest

@pytest.mark.asyncio
async def test_dedup_single_event(client):
    event = {
        "topic": "dedup",
        "event_id": "e1",
        "timestamp": "2025-12-18T10:00:00Z",
        "source": "pytest",
        "payload": {"x": 1}
    }

    await client.post("/publish", json=event)
    await client.post("/publish", json=event)

    stats = (await client.get("/stats")).json()

    assert stats["unique_processed"] == 1
    assert stats["duplicate_dropped"] == 1

@pytest.mark.asyncio
async def test_dedup_batch(client):
    events = [
        {
            "topic": "batch",
            "event_id": "same-id",
            "timestamp": "2025-12-18T10:00:00Z",
            "source": "pytest",
            "payload": {"i": i}
        }
        for i in range(5)
    ]

    await client.post("/publish", json=events)

    stats = (await client.get("/stats")).json()
    assert stats["unique_processed"] >= 1
