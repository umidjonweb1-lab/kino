from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import is_admin
from database.users import touch_last_active
from utils.subscription import is_user_subscribed
from utils.film_search import send_film_by_code
from handlers.start import send_subscription_prompt

router = Router(name="user")


@router.message(Command("admin"))
async def deny_admin_access(message: Message):
    # Bu handler faqat oddiy (admin bo'lmagan) foydalanuvchilar uchun ishlaydi,
    # chunki adminlar uchun /admin buyrug'i handlers/admin.py da to'xtatiladi.
    await message.answer("❌ Sizda admin huquqi mavjud emas.")


@router.message(F.text & ~F.text.startswith("/"))
async def handle_film_code(message: Message):
    # Admin xabarlarini admin panel handlerlariga qoldiramiz (bu yerga kelmasligi kerak,
    # chunki admin routerlar avval ro'yxatdan o'tadi, lekin himoya uchun tekshiramiz).
    if is_admin(message.from_user.id):
        return

    subscribed, not_subscribed = await is_user_subscribed(message.bot, message.from_user.id)
    if not subscribed:
        await send_subscription_prompt(message, not_subscribed)
        return

    await touch_last_active(message.from_user.id)

    film_code = message.text.strip()
    found = await send_film_by_code(message.bot, message, film_code)
    if not found:
        await message.answer("🚫 Bu kodga mos film topilmadi.")
