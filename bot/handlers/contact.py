from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes

from ..config import get_settings


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings()

    if settings.admin_chat_id is None:
        text = (
            "⚠️ Admin chat ID sozlanmagan.\n\n"
            "Iltimos, bot sozlamalarida ADMIN_CHAT_ID ni to'ldiring."
        )
        await update.message.reply_text(text)
        return

    text = (
        "📬 Savol yoki takliflaringiz bo'lsa, admin bilan bog'lanish uchun quyidagi tugmani bosing.\n\n"
        "Profil ochilgach, xabaringizni bevosita yozishingiz mumkin."
    )

    # Ko'p Telegram klientlarda tg://user?id=ID formati admin profilini ochadi
    url = f"tg://user?id={settings.admin_chat_id}"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="✉️ Admin bilan yozish", url=url)]]
    )

    await update.message.reply_text(text, reply_markup=keyboard)


def get_contact_handler() -> CommandHandler:
    return CommandHandler("contact", contact)
