from datetime import datetime
from database.database import get_db


async def add_or_update_user(telegram_id: int, username: str | None, full_name: str):
    db = await get_db()
    try:
        cur = await db.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
        row = await cur.fetchone()
        if row:
            await db.execute(
                "UPDATE users SET username = ?, full_name = ?, last_active = datetime('now') WHERE telegram_id = ?",
                (username, full_name, telegram_id),
            )
        else:
            await db.execute(
                "INSERT INTO users (telegram_id, username, full_name) VALUES (?, ?, ?)",
                (telegram_id, username, full_name),
            )
        await db.commit()
    finally:
        await db.close()


async def touch_last_active(telegram_id: int):
    db = await get_db()
    try:
        await db.execute(
            "UPDATE users SET last_active = datetime('now') WHERE telegram_id = ?",
            (telegram_id,),
        )
        await db.commit()
    finally:
        await db.close()


async def get_all_user_ids() -> list[int]:
    db = await get_db()
    try:
        cur = await db.execute("SELECT telegram_id FROM users")
        rows = await cur.fetchall()
        return [r[0] for r in rows]
    finally:
        await db.close()


async def get_stats() -> dict:
    db = await get_db()
    try:
        stats = {}
        cur = await db.execute("SELECT COUNT(*) FROM users")
        stats["total"] = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE last_active >= datetime('now', '-1 day')"
        )
        stats["active"] = (await cur.fetchone())[0]
        stats["inactive"] = stats["total"] - stats["active"]

        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE joined_at >= datetime('now', '-1 day')"
        )
        stats["new_today"] = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE joined_at >= datetime('now', '-7 day')"
        )
        stats["new_7d"] = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE joined_at >= datetime('now', '-30 day')"
        )
        stats["new_30d"] = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE last_active >= datetime('now', '-7 day')"
        )
        stats["active_7d"] = (await cur.fetchone())[0]

        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE last_active >= datetime('now', '-30 day')"
        )
        stats["active_30d"] = (await cur.fetchone())[0]

        return stats
    finally:
        await db.close()
