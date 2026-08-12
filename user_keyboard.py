from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def subscription_keyboard(channels: list[dict]) -> InlineKeyboardMarkup:
    """channels: list of {id, chat_id, username, title}"""
    builder = InlineKeyboardBuilder()
    for ch in channels:
        if ch["username"]:
            url = f"https://t.me/{ch['username'].lstrip('@')}"
        else:
            url = f"https://t.me/c/{str(ch['chat_id']).replace('-100', '')}"
        builder.row(InlineKeyboardButton(text=f"📢 {ch['title'] or ch['username']}", url=url))
    builder.row(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub"))
    return builder.as_markup()
