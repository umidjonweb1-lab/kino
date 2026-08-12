from aiogram.fsm.state import State, StatesGroup


class AdminFilter(StatesGroup):
    """Foydalanuvchi admin ekanini tekshirish uchun alohida filtr kerak emas,
    lekin FSM holatlari shu yerda saqlanadi."""


class UploadFilm(StatesGroup):
    code = State()
    title = State()
    video = State()
    poster = State()
    genre = State()
    language = State()
    year = State()
    description = State()


class EditFilm(StatesGroup):
    waiting_code = State()
    choosing_field = State()
    waiting_value = State()


class AddEpisode(StatesGroup):
    waiting_series_code = State()
    waiting_episode_number = State()
    waiting_video = State()


class Broadcast(StatesGroup):
    waiting_message = State()
    confirm = State()


class AddChannel(StatesGroup):
    waiting_channel = State()


class DeleteLink(StatesGroup):
    waiting_choice = State()


class AddLink(StatesGroup):
    waiting_name = State()
    waiting_url = State()
