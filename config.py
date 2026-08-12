import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

_admin_ids_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in _admin_ids_raw.split(",") if x.strip().isdigit()]

DB_PATH = os.getenv("DB_PATH", "kino_bot.db")


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
