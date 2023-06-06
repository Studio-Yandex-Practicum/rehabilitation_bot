from telegram.ext import Application

from bot.core.settings import settings
from bot.handlers import (
    greet_new_member_handler,
    main_handler,
    message_filter_handler,
    moderation_handler,
    moderation_spam_handler,
)


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = Application.builder().token(settings.telegram_token).build()
    application.add_handler(main_handler, group=0)
    application.add_handler(greet_new_member_handler, group=1)
    application.add_handler(message_filter_handler, group=2)
    application.add_handler(moderation_handler, group=3)
    application.add_handler(moderation_spam_handler, group=4)
    application.run_polling()


if __name__ == "__main__":
    main()
