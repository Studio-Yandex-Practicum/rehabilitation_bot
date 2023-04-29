from telegram.ext import Application, CommandHandler

from bot.core.settings import settings
from bot.conversations.main_application import start


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = Application.builder().token(settings.telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


if __name__ == "__main__":
    main()
