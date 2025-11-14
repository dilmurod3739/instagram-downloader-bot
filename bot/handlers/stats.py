import logging

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from ..config import get_settings
from ..db.database import get_connection

logger = logging.getLogger(__name__)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings()
    chat_id = update.effective_chat.id

    if settings.admin_chat_id is not None and settings.admin_chat_id != chat_id:
        await update.message.reply_text("⛔ Bu buyruq faqat admin uchun.")
        logger.info("/stats denied for chat_id=%s", chat_id)
        return

    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users")
        users_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM downloads")
        downloads_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM downloads WHERE status = 'success'")
        success_count = cur.fetchone()[0]

    text = (
        "📊 *Bot statistikasi*\n\n"
        f"👥 Foydalanuvchilar: {users_count}\n"
        f"⬇️ Yuklashlar (jami): {downloads_count}\n"
        f"✅ Muvaffaqiyatli yuklashlar: {success_count}\n"
    )

    await update.message.reply_text(text)
    logger.info("/stats shown to chat_id=%s", chat_id)


def get_stats_handler() -> CommandHandler:
    return CommandHandler("stats", stats)
