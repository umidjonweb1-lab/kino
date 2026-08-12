from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import is_admin
from database.films import (
    add_film, get_film_by_code, update_film_field, add_episode,
)
from handlers.states import UploadFilm, EditFilm, AddEpisode
from keyboards.admin_keyboard import admin_main_menu, cancel_keyboard, skip_keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

router = Router(name="films")
router.message.filter(lambda message: is_admin(message.from_user.id))
router.callback_query.filter(lambda cb: is_admin(cb.from_user.id))


# ---------- FILM YUKLASH ----------

@router.message(F.text == "🎬 Film yuklash")
async def start_upload(message: Message, state: FSMContext):
    await state.set_state(UploadFilm.code)
    await message.answer("1️⃣ Film kodini kiriting:", reply_markup=cancel_keyboard())


@router.message(UploadFilm.code)
async def upload_code(message: Message, state: FSMContext):
    code = message.text.strip()
    existing = await get_film_by_code(code)
    if existing:
        await message.answer("⚠️ Bu kod band. Boshqa kod kiriting:")
        return
    await state.update_data(code=code)
    await state.set_state(UploadFilm.title)
    await message.answer("2️⃣ Film nomini kiriting:")


@router.message(UploadFilm.title)
async def upload_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await state.set_state(UploadFilm.video)
    await message.answer("3️⃣ Film videosini yuboring:")


@router.message(UploadFilm.video, F.video)
async def upload_video(message: Message, state: FSMContext):
    await state.update_data(file_id=message.video.file_id)
    await state.set_state(UploadFilm.poster)
    await message.answer("4️⃣ Poster (rasm) yuboring (yoki o'tkazib yuboring):",
                          reply_markup=skip_keyboard())


@router.message(UploadFilm.video)
async def upload_video_invalid(message: Message):
    await message.answer("❗️ Iltimos, video fayl yuboring.")


@router.message(UploadFilm.poster, F.photo)
async def upload_poster(message: Message, state: FSMContext):
    await state.update_data(poster_file_id=message.photo[-1].file_id)
    await state.set_state(UploadFilm.genre)
    await message.answer("5️⃣ Janrini kiriting (yoki o'tkazib yuboring):", reply_markup=skip_keyboard())


@router.message(UploadFilm.poster, F.text == "➡️ O'tkazib yuborish")
async def skip_poster(message: Message, state: FSMContext):
    await state.update_data(poster_file_id=None)
    await state.set_state(UploadFilm.genre)
    await message.answer("5️⃣ Janrini kiriting (yoki o'tkazib yuboring):", reply_markup=skip_keyboard())


@router.message(UploadFilm.genre)
async def upload_genre(message: Message, state: FSMContext):
    value = None if message.text == "➡️ O'tkazib yuborish" else message.text.strip()
    await state.update_data(genre=value)
    await state.set_state(UploadFilm.language)
    await message.answer("6️⃣ Tilini kiriting (yoki o'tkazib yuboring):", reply_markup=skip_keyboard())


@router.message(UploadFilm.language)
async def upload_language(message: Message, state: FSMContext):
    value = None if message.text == "➡️ O'tkazib yuborish" else message.text.strip()
    await state.update_data(language=value)
    await state.set_state(UploadFilm.year)
    await message.answer("7️⃣ Yilini kiriting (yoki o'tkazib yuboring):", reply_markup=skip_keyboard())


@router.message(UploadFilm.year)
async def upload_year(message: Message, state: FSMContext):
    value = None if message.text == "➡️ O'tkazib yuborish" else message.text.strip()
    await state.update_data(year=value)
    await state.set_state(UploadFilm.description)
    await message.answer("8️⃣ Tavsifini kiriting (yoki o'tkazib yuboring):", reply_markup=skip_keyboard())


@router.message(UploadFilm.description)
async def upload_description(message: Message, state: FSMContext):
    value = None if message.text == "➡️ O'tkazib yuborish" else message.text.strip()
    await state.update_data(description=value)
    data = await state.get_data()

    ok = await add_film(
        film_code=data["code"],
        title=data["title"],
        file_id=data["file_id"],
        poster_file_id=data.get("poster_file_id"),
        genre=data.get("genre"),
        language=data.get("language"),
        year=data.get("year"),
        description=value,
    )
    await state.clear()

    if ok:
        await message.answer(
            f"✅ Film muvaffaqiyatli saqlandi!\n🔑 Kod: {data['code']}",
            reply_markup=admin_main_menu(),
        )
    else:
        await message.answer("❌ Xatolik yuz berdi, qaytadan urinib ko'ring.", reply_markup=admin_main_menu())


# ---------- FILM TAHRIRLASH ----------

@router.message(F.text == "✏️ Film tahrirlash")
async def start_edit(message: Message, state: FSMContext):
    await state.set_state(EditFilm.waiting_code)
    await message.answer("✏️ Tahrirlash uchun film kodini yuboring:", reply_markup=cancel_keyboard())


@router.message(EditFilm.waiting_code)
async def edit_find_film(message: Message, state: FSMContext):
    code = message.text.strip()
    film = await get_film_by_code(code)
    if not film:
        await message.answer("🚫 Bu kodga mos film topilmadi. Qayta kiriting:")
        return

    await state.update_data(code=code)
    await state.set_state(EditFilm.choosing_field)

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📝 Nomi", callback_data="editf_title"))
    builder.row(InlineKeyboardButton(text="🎥 Video", callback_data="editf_file_id"))
    builder.row(InlineKeyboardButton(text="🖼 Poster", callback_data="editf_poster_file_id"))
    builder.row(InlineKeyboardButton(text="📄 Tavsif", callback_data="editf_description"))
    builder.row(InlineKeyboardButton(text="🔑 Kod", callback_data="editf_film_code"))
    await message.answer(f"«{film['title']}» — nimani tahrirlaysiz?", reply_markup=builder.as_markup())


FIELD_LABELS = {
    "title": "nomini",
    "file_id": "videosini",
    "poster_file_id": "posterini",
    "description": "tavsifini",
    "film_code": "kodini",
}
FIELD_PROMPTS = {
    "title": "Yangi nomni yuboring:",
    "file_id": "Yangi videoni yuboring:",
    "poster_file_id": "Yangi posterni (rasm) yuboring:",
    "description": "Yangi tavsifni yuboring:",
    "film_code": "Yangi kodni yuboring:",
}


@router.callback_query(EditFilm.choosing_field, F.data.startswith("editf_"))
async def choose_field(callback, state: FSMContext):
    field = callback.data.removeprefix("editf_")
    await state.update_data(field=field)
    await state.set_state(EditFilm.waiting_value)
    await callback.message.answer(FIELD_PROMPTS[field], reply_markup=cancel_keyboard())
    await callback.answer()


@router.message(EditFilm.waiting_value, F.video)
async def edit_value_video(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["field"] != "file_id":
        await message.answer("❗️ Video emas, matn kutilmoqda.")
        return
    await _apply_edit(message, state, message.video.file_id)


@router.message(EditFilm.waiting_value, F.photo)
async def edit_value_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["field"] != "poster_file_id":
        await message.answer("❗️ Rasm emas, matn kutilmoqda.")
        return
    await _apply_edit(message, state, message.photo[-1].file_id)


@router.message(EditFilm.waiting_value, F.text)
async def edit_value_text(message: Message, state: FSMContext):
    data = await state.get_data()
    if data["field"] in ("file_id", "poster_file_id"):
        await message.answer("❗️ Fayl yuborish kerak.")
        return
    if data["field"] == "film_code":
        existing = await get_film_by_code(message.text.strip())
        if existing:
            await message.answer("⚠️ Bu kod band. Boshqa kod kiriting:")
            return
    await _apply_edit(message, state, message.text.strip())


async def _apply_edit(message: Message, state: FSMContext, value):
    data = await state.get_data()
    await update_film_field(data["code"], data["field"], value)
    await state.clear()
    label = FIELD_LABELS.get(data["field"], data["field"])
    await message.answer(f"✅ Film {label} muvaffaqiyatli yangilandi.", reply_markup=admin_main_menu())


# ---------- SERIALGA QISM QO'SHISH ----------

@router.message(F.text == "➕ Serialga qo'shimcha qism qo'shish")
async def start_add_episode(message: Message, state: FSMContext):
    await state.set_state(AddEpisode.waiting_series_code)
    await message.answer("🎞 Serial kodini kiriting:", reply_markup=cancel_keyboard())


@router.message(AddEpisode.waiting_series_code)
async def episode_series_code(message: Message, state: FSMContext):
    code = message.text.strip()
    film = await get_film_by_code(code)
    if not film:
        await message.answer("🚫 Bu kodga mos serial topilmadi. Qayta kiriting:")
        return
    await state.update_data(film_id=film["id"], title=film["title"])
    await state.set_state(AddEpisode.waiting_episode_number)
    await message.answer("🔢 Qism raqamini kiriting:")


@router.message(AddEpisode.waiting_episode_number)
async def episode_number(message: Message, state: FSMContext):
    if not message.text.strip().isdigit():
        await message.answer("❗️ Faqat raqam kiriting:")
        return
    await state.update_data(episode_number=int(message.text.strip()))
    await state.set_state(AddEpisode.waiting_video)
    await message.answer("🎥 Qism videosini yuboring:")


@router.message(AddEpisode.waiting_video, F.video)
async def episode_video(message: Message, state: FSMContext):
    data = await state.get_data()
    ok = await add_episode(data["film_id"], data["episode_number"], message.video.file_id)
    await state.clear()
    if ok:
        await message.answer(
            f"✅ «{data['title']}» — {data['episode_number']}-qism qo'shildi.",
            reply_markup=admin_main_menu(),
        )
    else:
        await message.answer(
            "⚠️ Bu qism raqami allaqachon mavjud yoki xatolik yuz berdi.",
            reply_markup=admin_main_menu(),
        )


@router.message(AddEpisode.waiting_video)
async def episode_video_invalid(message: Message):
    await message.answer("❗️ Iltimos, video fayl yuboring.")
