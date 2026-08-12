from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from database.users import add_or_update_user
from keyboards.user_keyboard import subscription_keyboard
from utils.subscription import is_user_subscribed

router = Router(name="start")


async def send_subscription_prompt(message_or_cb, not_subscribed: list[dict]):
    text = "🔒 Botdan foydalanish uchun quyidagi kanal(lar)ga a'zo bo'ling!"
    kb = subscription_keyboard(not_subscribed)
    if isinstance(message_or_cb, Message):
        await message_or_cb.answer(text, reply_markup=kb)
    else:
        await message_or_cb.message.answer(text, reply_markup=kb)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_or_update_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )

    subscribed, not_subscribed = await is_user_subscribed(message.bot, message.from_user.id)
    if not subscribed:
        await send_subscription_prompt(message, not_subscribed)
        return

    await message.answer(
        f"👋 Assalomu alaykum, {message.from_user.full_name}!\n\n"
        f"✍️ Marhamat, film kodini yuboring."
    )


@router.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    subscribed, not_subscribed = await is_user_subscribed(callback.bot, callback.from_user.id)
    if not subscribed:
        await callback.answer("❌ Avval kanalga obuna bo'ling.", show_alert=True)
        return

    await callback.message.edit_text("✅ Obuna tasdiqlandi.\n\n✍️ Film kodini yuboring.")
    await callback.answer()
