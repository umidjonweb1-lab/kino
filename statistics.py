import asyncio
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import is_admin
from database.users import get_stats, get_all_user_ids
from database.films import get_top_films
from handlers.states import Broadcast
from keyboards.admin_keyboard import cancel_keyboard, admin_main_menu

router = Router(name="statistics")
router.message.filter(lambda message: is_admin(message.from_user.id))


@router.message(F.text == "📊 Statistika")
async def show_stats(message: Message):
    s = await get_stats()
    text = (
        "📊 <b>Foydalanuvchilar statistikasi</b>\n\n"
        f"👥 Jami: {s['total']} ta\n\n"
        f"• Faol (24 soat): {s['active']} ta\n"
        f"• Nofaol: {s['inactive']} ta\n\n"
        "🆕 Yangi obunachilar:\n"
        f"• Bugungi: {s['new_today']} ta\n"
        f"• 7 kunlik: {s['new_7d']} ta\n"
        f"• 30 kunlik: {s['new_30d']} ta\n\n"
        "🔥 Foydalanuvchilar aktivligi:\n"
        f"• 7 kunlik: {s['active_7d']} ta\n"
        f"• 30 kunlik: {s['active_30d']} ta\n"
    )
    await message.answer(text)


@router.message(F.text == "🔝 Top filmlar")
async def top_films(message: Message):
    films = await get_top_films(10)
    if not films:
        await message.answer("📭 Hozircha filmlar mavjud emas.")
        return
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    text = "🔥 <b>TOP FILMLAR</b>\n\n"
    for i, f in enumerate(films):
        text += f"{emojis[i] if i < 10 else i+1} {f['title']} — {f['views']} ko'rildi\n"
    await message.answer(text)


@router.message(F.text == "✉️ Xabarnoma")
async def broadcast_start(message: Message, state: FSMContext):
    await state.set_state(Broadcast.waiting_message)
    await message.answer("✉️ Yuboriladigan xabarni kiriting:", reply_markup=cancel_keyboard())


@router.message(Broadcast.waiting_message)
async def broadcast_send(message: Message, state: FSMContext):
    await state.clear()
    user_ids = await get_all_user_ids()
    await message.answer(f"⏳ {len(user_ids)} ta foydalanuvchiga yuborilmoqda...")

    sent, failed = 0, 0
    for uid in user_ids:
        try:
            await message.copy_to(chat_id=uid)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # flood limitdan saqlanish

    await message.answer(
        f"✅ Xabarnoma yuborildi.\n\n📤 Yuborildi: {sent} ta\n❌ Yuborilmadi: {failed} ta",
        reply_markup=admin_main_menu(),
    )
