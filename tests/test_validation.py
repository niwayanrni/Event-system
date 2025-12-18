# tests/test_validation.py
import pytest

@pytest.mark.asyncio
async def test_invalid_schema(client):
    res = await client.post("/publish", json={"foo": "bar"})
    assert res.status_code == 422
