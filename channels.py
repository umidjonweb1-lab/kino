from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import is_admin
from database.channels import add_channel, remove_channel, get_all_channels
from handlers.states import AddChannel
from keyboards.admin_keyboard import (
    channels_menu, mandatory_sub_menu, cancel_keyboard, admin_main_menu, channel_delete_inline,
)

router = Router(name="channels")
router.message.filter(lambda message: is_admin(message.from_user.id))
router.callback_query.filter(lambda cb: is_admin(cb.from_user.id))


@router.message(F.text == "📢 Kanallarni sozlash")
async def channels_settings(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📢 Kanallarni sozlash:", reply_markup=channels_menu())


@router.message(F.text == "🔒 Majburiy obuna")
async def mandatory_sub_settings(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🔒 Majburiy obuna sozlamalari:", reply_markup=mandatory_sub_menu())


@router.message(F.text == "➕ Kanal qo'shish")
async def add_channel_start(message: Message, state: FSMContext):
    await state.set_state(AddChannel.waiting_channel)
    await message.answer(
        "🔗 Kanal username (@kanal) yoki ID sini yuboring.\n"
        "❗️ Bot kanalda admin bo'lishi shart.",
        reply_markup=cancel_keyboard(),
    )


@router.message(AddChannel.waiting_channel)
async def add_channel_finish(message: Message, state: FSMContext):
    chat_id_input = message.text.strip()
    try:
        chat = await message.bot.get_chat(chat_id_input)
    except Exception:
        await message.answer("❌ Kanal topilmadi yoki bot u yerda admin emas. Qayta urinib ko'ring:")
        return

    ok = await add_channel(
        chat_id=str(chat.id),
        username=chat.username,
        title=chat.title,
        channel_type="mandatory",
    )
    await state.clear()
    if ok:
        await message.answer(f"✅ Kanal qo'shildi: {chat.title}", reply_markup=mandatory_sub_menu())
    else:
        await message.answer("⚠️ Bu kanal allaqachon qo'shilgan.", reply_markup=mandatory_sub_menu())


@router.message(F.text == "📋 Kanallar ro'yxati")
async def list_channels(message: Message):
    channels = await get_all_channels()
    if not channels:
        await message.answer("📭 Hozircha kanallar yo'q.")
        return
    text = "📋 Ulangan kanallar:\n\n"
    for ch in channels:
        label = ch["title"] or ch["username"] or ch["chat_id"]
        text += f"• {label} ({ch['channel_type']})\n"
    await message.answer(text)


@router.message(F.text == "🗑 Kanal o'chirish")
async def delete_channel_menu(message: Message):
    channels = await get_all_channels()
    if not channels:
        await message.answer("📭 O'chirish uchun kanallar yo'q.")
        return
    await message.answer("🗑 O'chirmoqchi bo'lgan kanalni tanlang:", reply_markup=channel_delete_inline(channels))


@router.callback_query(F.data.startswith("delch_"))
async def delete_channel_confirm(callback: CallbackQuery):
    channel_id = int(callback.data.removeprefix("delch_"))
    await remove_channel(channel_id)
    await callback.message.edit_text("✅ Kanal o'chirildi.")
    await callback.answer()
