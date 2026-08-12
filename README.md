# 🎬 Kino Telegram Bot

Film kodi orqali qidiriladigan, majburiy obuna va to'liq admin panelga ega Telegram bot.
Python + [aiogram 3](https://docs.aiogram.dev/) + SQLite asosida yozilgan.

## 📦 O'rnatish

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Sozlash

1. `.env.example` faylini nusxalab `.env` deb saqlang:
   ```bash
   cp .env.example .env
   ```
2. `.env` faylini oching va to'ldiring:
   ```
   BOT_TOKEN=123456:AA...      # @BotFather dan olingan token
   ADMIN_IDS=123456789         # sizning Telegram ID(lar)ingiz, vergul bilan
   ```
   O'z Telegram ID ingizni bilish uchun @userinfobot ga yozing.

## ▶️ Ishga tushirish

```bash
python main.py
```

## 🗂 Loyiha tuzilishi

```
kino_bot/
├── main.py                 # Botni ishga tushiruvchi asosiy fayl
├── config.py                # Token, admin ID lar
├── database/
│   ├── database.py           # SQLite ulanish va jadval yaratish
│   ├── users.py               # Foydalanuvchilar bilan ishlash
│   ├── films.py                # Filmlar va serial qismlari
│   ├── channels.py             # Majburiy obuna kanallari
│   └── settings.py              # Umumiy sozlamalar (key-value)
├── handlers/
│   ├── start.py                # /start, majburiy obuna tekshiruvi
│   ├── user.py                  # Film kodi qabul qilish
│   ├── admin.py                  # /admin, asosiy panel
│   ├── films.py                   # Film yuklash / tahrirlash / serial qism
│   ├── channels.py                 # Kanallarni boshqarish
│   ├── statistics.py                # Statistika, top filmlar, xabarnoma
│   └── states.py                     # FSM holatlari
├── keyboards/
│   ├── user_keyboard.py        # Obuna klaviaturasi
│   └── admin_keyboard.py        # Admin panel klaviaturalari
└── utils/
    ├── subscription.py         # Majburiy obunani tekshirish
    └── film_search.py           # Kod bo'yicha film topib yuborish
```

## ✅ Hozircha ishlaydigan funksiyalar

- `/start`, majburiy obuna tekshiruvi (kanalga a'zolikni Telegram API orqali tekshiradi)
- Film kodi bo'yicha qidirish va yuborish (poster + video, serial bo'lsa barcha qismlar)
- Admin panel: 🎬 Film yuklash, ✏️ Film tahrirlash, ➕ Serial qismi qo'shish
- ✉️ Xabarnoma (barcha foydalanuvchilarga broadcast)
- 📊 Statistika (jami/faol/nofaol, yangi obunachilar, aktivlik)
- 🔝 Top filmlar (ko'rishlar soni bo'yicha)
- ⚙️ Bot sozlamalari → 📢 Kanallarni sozlash → 🔒 Majburiy obuna (qo'shish/o'chirish/ro'yxat)

## 🚧 Keyingi bosqichda qo'shsa bo'ladigan qismlar

Spetsifikatsiyada ko'rsatilgan quyidagi bo'limlar hozircha **skelet** holatida (`settings` jadvali orqali kengaytirish mumkin):

- 🔗 Qo'shimcha linklar (jadval bazada tayyor: `links`)
- 💎 VIP tizimi va 💵 RUB narxlari (`users.is_vip`, `users.vip_until` ustunlari tayyor)
- 💳 To'lov tizimlari va ⚡ Avto to'lov
- 🗄 Baza kanalidan film postlarini olish
- 🛡 Film uzatish usulini (forward/copy) sozlash

Bularning har biri alohida so'ralsa, mavjud tuzilmaga mos qilib qo'shib beraman.

## 🔐 Xavfsizlik eslatmasi

- Bot tokenini hech qachon kodga yozib qo'ymang — faqat `.env` orqali bering.
- `ADMIN_IDS` ro'yxatiga faqat ishonchli shaxslarni qo'shing.
