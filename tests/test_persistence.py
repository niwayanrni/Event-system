# tests/test_persistence.py
import pytest

@pytest.mark.asyncio
async def test_persistence(client):
    event = {
        "topic": "persist",
        "event_id": "p1",
        "timestamp": "2025-12-18T10:00:00Z",
        "source": "pytest",
        "payload": {}
    }

    await client.post("/publish", json=event)
    await client.post("/publish", json=event)

    stats = (await client.get("/stats")).json()
    assert stats["unique_processed"] == 1
