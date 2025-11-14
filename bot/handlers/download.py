from urllib.parse import urlparse

from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters

from ..config import get_settings
from ..db.database import log_download
from ..services.instagram_downloader import RateLimitError, fetch_instagram_media


def _is_instagram_url(text: str) -> bool:
    lowered = text.lower()
    return "instagram.com" in lowered


def _guess_media_type(media_url: str) -> str:
    path = urlparse(media_url).path.lower()
    if path.endswith((".mp4", ".mov", ".mkv", ".webm")):
        return "video"
    if path.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
        return "photo"
    return "file"


async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    url = update.message.text.strip()

    if not _is_instagram_url(url):
        await update.message.reply_text(
            "❗ Iltimos, faqat Instagram post yoki reels linkini yuboring (instagram.com/... )."
        )
        log_download(chat_id=chat_id, instagram_url=url, status="invalid_url", error_message="not_instagram")
        return

    await update.message.chat.send_action(action="upload_document")

    try:
        media_urls = await fetch_instagram_media(url)
    except RateLimitError as exc:
        log_download(chat_id=chat_id, instagram_url=url, status="rate_limit", error_message=str(exc))

        await update.message.reply_text(
            "⏱ API limiti vaqtincha tugadi. Iltimos, birozdan so'ng qayta urinib ko'ring."
        )

        settings = get_settings()
        if settings.admin_chat_id is not None:
            # Adminga texnik xabar
            try:
                await context.bot.send_message(
                    chat_id=settings.admin_chat_id,
                    text=(
                        "⚠️ RapidAPI rate limit tugadi.\n\n"
                        f"User chat_id: {chat_id}\n"
                        f"URL: {url}"
                    ),
                )
            except Exception:
                # Admin'ga xabar yuborishda xato bo'lsa, foydalanuvchi uchun muhim emas
                pass

        return
    except Exception as exc:
        log_download(chat_id=chat_id, instagram_url=url, status="error", error_message=str(exc))
        await update.message.reply_text(
            "⚠️ Serverda kutilmagan xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring."
        )
        return

    if not media_urls:
        log_download(chat_id=chat_id, instagram_url=url, status="no_media", error_message="empty_result")
        await update.message.reply_text(
            "🔍 Media topilmadi yoki link noto'g'ri. Iltimos, linkni tekshirib qayta yuboring."
        )
        return

    sent_any = False

    for index, media_url in enumerate(media_urls, start=1):
        media_type = _guess_media_type(media_url)

        caption_lines = []
        if media_type == "video":
            caption_lines.append("🎬 Video")
        elif media_type == "photo":
            caption_lines.append("🖼 Rasm")
        else:
            caption_lines.append("📎 Fayl")

        if len(media_urls) > 1:
            caption_lines.append(f"(fayl {index}/{len(media_urls)})")

        caption_lines.append("")
        caption_lines.append(f"🔗 Asl post: {url}")

        caption = "\n".join(caption_lines)

        try:
            if media_type == "video":
                await update.message.reply_video(video=media_url, caption=caption)
            elif media_type == "photo":
                await update.message.reply_photo(photo=media_url, caption=caption)
            else:
                await update.message.reply_document(document=media_url, caption=caption)
            sent_any = True
        except Exception:
            continue

    if sent_any:
        log_download(chat_id=chat_id, instagram_url=url, status="success")
    else:
        log_download(chat_id=chat_id, instagram_url=url, status="error", error_message="send_failed")
        await update.message.reply_text(
            "⚠️ Media topildi, lekin Telegram orqali yuborishda xatolik yuz berdi. Keyinroq qayta urinib ko'ring."
        )


def get_download_handler() -> MessageHandler:
    return MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link)
