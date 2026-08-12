from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import is_admin
from keyboards.admin_keyboard import admin_main_menu, settings_menu

router = Router(name="admin")

# Faqat admin ID lariga ruxsat berish
router.message.filter(lambda message: is_admin(message.from_user.id))


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ ADMIN PANELI", reply_markup=admin_main_menu())


@router.message(F.text == "◀️ Orqaga")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ ADMIN PANELI", reply_markup=admin_main_menu())


@router.message(F.text == "❌ Bekor qilish")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.", reply_markup=admin_main_menu())


@router.message(F.text == "⚙️ Bot sozlamalari")
async def settings_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("⚙️ Bot sozlamalari:", reply_markup=settings_menu())
