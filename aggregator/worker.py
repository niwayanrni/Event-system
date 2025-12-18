import asyncio
import json
import redis

redis_client = redis.Redis(host="broker", port=6379, decode_responses=True)

async def worker(pool, worker_id):
    print(f"👷 Worker {worker_id} started")

    while True:
        item = redis_client.lpop("events")
        if not item:
            await asyncio.sleep(0.5)  # 🔥 WAJIB
            continue

        event = json.loads(item)

        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE stats SET value = value + 1 WHERE key='received'"
            )

            try:
                await conn.execute("""
                INSERT INTO processed_events (topic, event_id, payload)
                VALUES ($1, $2, $3)
                """, event["topic"], event["event_id"], json.dumps(event["payload"]))

                await conn.execute(
                    "UPDATE stats SET value = value + 1 WHERE key='unique_processed'"
                )
            except:
                await conn.execute(
                    "UPDATE stats SET value = value + 1 WHERE key='duplicate_dropped'"
                )
