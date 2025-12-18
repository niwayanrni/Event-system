from fastapi import FastAPI, Query, Body
import redis, asyncio, json
from database import create_pool
from worker import worker

app = FastAPI()
redis_client = redis.Redis(host="broker", port=6379, decode_responses=True)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/stats")
async def stats():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch("SELECT key, value FROM stats")
    return {r["key"]: r["value"] for r in rows}

@app.get("/events")
async def get_events(topic: str = Query(...)):
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT topic, event_id, payload
            FROM processed_events
            WHERE topic = $1
            ORDER BY event_id
            """,
            topic
        )

    return [
        {
            "topic": r["topic"],
            "event_id": r["event_id"],
            "payload": r["payload"]
        }
        for r in rows
    ]

@app.on_event("startup")
async def startup():
    app.state.pool = await create_pool()
    print("✅ DB connected")

    async with app.state.pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            key TEXT PRIMARY KEY,
            value INT
        )
        """)

        await conn.execute("""
        INSERT INTO stats (key, value) VALUES
        ('received', 0),
        ('unique_processed', 0),
        ('duplicate_dropped', 0)
        ON CONFLICT (key) DO NOTHING
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS processed_events (
            id SERIAL PRIMARY KEY,
            topic TEXT,
            event_id TEXT UNIQUE,
            payload JSONB
        )
        """)

    await asyncio.sleep(3)

    for i in range(2):
        asyncio.create_task(worker(app.state.pool, i))

    print("🚀 Aggregator READY")

@app.post("/publish")
async def publish(event: dict = Body(...)):
    redis_client.lpush("events", json.dumps(event))
    return {"status": "queued"}

