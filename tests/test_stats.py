# tests/test_stats.py
import pytest

@pytest.mark.asyncio
async def test_stats_keys(client):
    res = await client.get("/stats")
    data = res.json()

    assert "received" in data
    assert "unique_processed" in data
    assert "duplicate_dropped" in data
