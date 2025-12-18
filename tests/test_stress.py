# tests/test_stress.py
import pytest

@pytest.mark.asyncio
async def test_small_stress(client):
    events = [
        {
            "topic": "stress",
            "event_id": str(i),
            "timestamp": "2025-12-18T10:00:00Z",
            "source": "pytest",
            "payload": {}
        }
        for i in range(300)
    ]

    res = await client.post("/publish", json=events)
    assert res.status_code == 200
