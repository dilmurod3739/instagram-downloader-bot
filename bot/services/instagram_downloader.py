from typing import List

import httpx

from ..config import get_settings


class RateLimitError(Exception):
    """RapidAPI limiti tugaganda ko'tariladigan istisno."""


async def fetch_instagram_media(instagram_url: str) -> List[str]:
    """RapidAPI orqali Instagram media link(lar)ini olish.

    Natija sifatida bevosita yuklab olinadigan URL'lar ro'yxati qaytariladi.
    """

    settings = get_settings()

    headers = {
        "x-rapidapi-key": settings.rapidapi_key,
        "x-rapidapi-host": settings.rapidapi_host,
    }

    params = {"url": instagram_url}

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(
                settings.rapidapi_url,
                headers=headers,
                params=params,
            )
            # raise_for_status 429 holatini ham HTTPStatusError sifatida ko'taradi
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response is not None and exc.response.status_code == 429:
                # RapidAPI limiti tugagan bo'lishi mumkin
                raise RateLimitError("RapidAPI rate limit reached") from exc
            # Boshqa HTTP status xatolari uchun bo'sh ro'yxat qaytaramiz
            return []
        except httpx.HTTPError:
            # Tarmoqdagi boshqa xatolar
            return []

    data = response.json()

    # Bu joyni siz tanlagan RapidAPI servisining aniq javob formatiga qarab moslashtirasiz.
    # Hozircha umumiy holda ba'zi keng tarqalgan maydonlarni tekshirib ko'ramiz.
    media_urls: List[str] = []

    if isinstance(data, dict):
        # 1) Agar 'media' maydonida ro'yxat bo'lsa
        media = data.get("media")
        if isinstance(media, list):
            for item in media:
                if isinstance(item, dict) and "url" in item:
                    media_urls.append(item["url"])
        # 2) Agar to'g'ridan-to'g'ri 'url' berilsa
        if not media_urls and "url" in data and isinstance(data["url"], str):
            media_urls.append(data["url"])

    return media_urls
