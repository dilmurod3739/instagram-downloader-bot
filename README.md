# Instagram Video Downloader Bot (Python + Telegram + RapidAPI)

## Loyihaning maqsadi

Ushbu bot foydalanuvchidan Instagram post/reels/stories linkini qabul qilib, RapidAPI orqali media (video/rasm) URL'larini oladi va foydalanuvchiga yuboradi.

## Texnologiyalar

- Python
- [python-telegram-bot](https://python-telegram-bot.org/) (async versiya)
- [httpx](https://www.python-httpx.org/) (HTTP so'rovlar)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (`.env` dan konfiguratsiya yuklash)
- RapidAPI'dagi Instagram downloader API

## Loyiha tuzilmasi

```bash
.
├── bot
│   ├── __init__.py
│   ├── main.py              # Botni ishga tushirish
│   ├── config.py            # .env dan sozlamalar
│   ├── keyboards
│   │   ├── __init__.py
│   │   └── common.py        # Klaviaturalar (inline/reply)
│   ├── handlers
│   │   ├── __init__.py
│   │   ├── start.py         # /start komandasi
│   │   └── download.py      # Foydalanuvchi yuborgan linkni qayta ishlash
│   └── services
│       ├── __init__.py
│       └── instagram_downloader.py  # RapidAPI bilan ishlovchi servis
├── .env.example             # Sozlamalar namunasi
├── requirements.txt         # Python kutubxonalari ro'yxati
└── README.md
```

## O'rnatish

1. **Virtual environment** (venv) yaratish (Windows):

```bash
python -m venv venv
venv\Scripts\activate
```

2. **Kutubxonalarni o'rnatish**:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **.env faylini sozlash**:

`.env.example` asosida `.env` yarating:

```bash
copy .env.example .env
```

So'ng `.env` ichini o'zgartiring:

- `TELEGRAM_BOT_TOKEN` – Telegram BotFather'dan olingan token
- `RAPIDAPI_KEY` – RapidAPI akkauntingizdagi API key
- `RAPIDAPI_HOST` – RapidAPI servisining host qiymati (header uchun)
- `RAPIDAPI_URL` – RapidAPI endpoint URL'i (Instagram downloader)

RapidAPI'dan tanlagan servisda odatda quyidagilar bo'ladi:

- Base URL (`RAPIDAPI_URL`)
- `x-rapidapi-key` header
- `x-rapidapi-host` header

Shularni mos ravishda `.env` ga yozing.

## Botni ishga tushirish

```bash
venv\Scripts\activate
python -m bot.main
```

Bot ishga tushgach, Telegram'da botga kirib `/start` yuboring va so'ng Instagram link yuboring.

## RapidAPI javob formatini moslashtirish

`bot/services/instagram_downloader.py` faylida `fetch_instagram_media` funksiyasi RapidAPI javobini quyidagicha faraz qiladi:

- `data["media"]` – ro'yxat, har bir elementida `"url"` maydoni bor, **yoki**
- `data["url"]` – bitta string URL

Agar siz tanlagan RapidAPI servicening JSON formatida farq bo'lsa, ushbu faylda `media_urls` yig'iladigan qismlarni o'zingiz moslab chiqishingiz kerak bo'ladi.

## Kengaytirish

- Yana qo'shimcha komandalar (`/help`, `/about` va boshqalar) uchun `bot/handlers/` ichida alohida modul oching.
- Klaviaturalarni bo'lib chiqish uchun `bot/keyboards/` ichida yangi fayllar yarating.
- Turli xil Instagram kontent turlarini (reels, stories, album) ajratish uchun servis qatlamini kengaytirish mumkin.
