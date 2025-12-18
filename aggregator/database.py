import asyncpg
import asyncio
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_pool():
    while True:
        try:
            pool = await asyncpg.create_pool(DATABASE_URL)
            print("✅ Database connected")
            return pool
        except Exception as e:
            print(f"⏳ Waiting for DB: {e}")
            await asyncio.sleep(2)
