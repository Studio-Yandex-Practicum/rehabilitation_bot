from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.constants.info.text import MESSAGE


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MESSAGE)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token("5865441282:AAEl6QkGcjRfvBWveLScisavjarxPvcJqo8").build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == "__main__":
    main()
