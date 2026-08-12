from aiogram import Bot
from aiogram.types import Message
from database.films import get_film_by_code, increment_views, get_episodes


async def send_film_by_code(bot: Bot, message: Message, film_code: str) -> bool:
    """Kod bo'yicha film topib yuboradi. Topilmasa False qaytaradi."""
    film = await get_film_by_code(film_code.strip())
    if film is None:
        return False

    caption = f"🎬 <b>{film['title']}</b>\n"
    if film.get("year"):
        caption += f"🗓 Yili: {film['year']}\n"
    if film.get("genre"):
        caption += f"🎭 Janr: {film['genre']}\n"
    if film.get("language"):
        caption += f"🗣 Til: {film['language']}\n"
    if film.get("description"):
        caption += f"\n📝 {film['description']}\n"
    caption += f"\n🔑 Kod: <code>{film['film_code']}</code>"

    if film["poster_file_id"]:
        await bot.send_photo(chat_id=message.chat.id, photo=film["poster_file_id"], caption=caption)
    else:
        await bot.send_message(chat_id=message.chat.id, text=caption)

    await bot.send_video(chat_id=message.chat.id, video=film["file_id"], caption=film["title"])

    if film.get("is_series"):
        episodes = await get_episodes(film["id"])
        for ep in episodes:
            await bot.send_video(
                chat_id=message.chat.id,
                video=ep["file_id"],
                caption=f"{film['title']} — {ep['episode_number']}-qism",
            )

    await increment_views(film["film_code"])
    return True
