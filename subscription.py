from aiogram import Bot
from database.channels import get_mandatory_channels


async def is_user_subscribed(bot: Bot, user_id: int) -> tuple[bool, list[dict]]:
    """Foydalanuvchi barcha majburiy kanallarga a'zo bo'lsa True, aks holda
    a'zo bo'lmagan kanallar ro'yxati bilan False qaytaradi."""
    channels = await get_mandatory_channels()
    if not channels:
        return True, []

    not_subscribed = []
    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch["chat_id"], user_id=user_id)
            if member.status in ("left", "kicked"):
                not_subscribed.append(ch)
        except Exception:
            # Bot kanalda admin bo'lmasa yoki kanal noto'g'ri bo'lsa, xatoni yutib yuboramiz
            not_subscribed.append(ch)

    return (len(not_subscribed) == 0), not_subscribed
