async def increment(conn, key, value=1):
    await conn.execute(
        "UPDATE stats SET value = value + $1 WHERE key = $2",
        value, key
    )
