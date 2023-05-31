from telegram.ext import Application

from bot.core.settings import settings
from bot.handlers import (main_handler, moderation_handler,
                          moderation_spam_handler)


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = Application.builder().token(settings.telegram_token).build()
    application.add_handler(main_handler)
    application.add_handler(moderation_handler, group=0)
    application.add_handler(moderation_spam_handler, group=1)

    application.run_polling()


if __name__ == "__main__":
    main()
