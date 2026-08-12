from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def admin_main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🎬 Film yuklash"), KeyboardButton(text="✏️ Film tahrirlash"))
    builder.row(KeyboardButton(text="➕ Serialga qo'shimcha qism qo'shish"))
    builder.row(KeyboardButton(text="✉️ Xabarnoma"), KeyboardButton(text="📊 Statistika"))
    builder.row(KeyboardButton(text="⚙️ Bot sozlamalari"))
    return builder.as_markup(resize_keyboard=True)


def settings_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="📢 Kanallarni sozlash"))
    builder.row(KeyboardButton(text="🔝 Top filmlar"))
    builder.row(KeyboardButton(text="◀️ Orqaga"))
    return builder.as_markup(resize_keyboard=True)


def channels_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🔒 Majburiy obuna"))
    builder.row(KeyboardButton(text="🔗 Qo'shimcha linklar"))
    builder.row(KeyboardButton(text="◀️ Orqaga"))
    return builder.as_markup(resize_keyboard=True)


def mandatory_sub_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="➕ Kanal qo'shish"), KeyboardButton(text="🗑 Kanal o'chirish"))
    builder.row(KeyboardButton(text="📋 Kanallar ro'yxati"))
    builder.row(KeyboardButton(text="◀️ Orqaga"))
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="❌ Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)


def skip_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="➡️ O'tkazib yuborish"))
    builder.row(KeyboardButton(text="❌ Bekor qilish"))
    return builder.as_markup(resize_keyboard=True)


def channel_delete_inline(channels: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ch in channels:
        label = ch["title"] or ch["username"] or ch["chat_id"]
        builder.row(InlineKeyboardButton(text=f"🗑 {label}", callback_data=f"delch_{ch['id']}"))
    return builder.as_markup()
