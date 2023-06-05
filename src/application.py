from telegram.ext import Application

from bot.core import logger  # noqa
from bot.core.settings import settings
from bot.handlers import main_handler, greet_new_member_handler


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = Application.builder().token(settings.telegram_token).build()
    application.add_handlers([main_handler, greet_new_member_handler])
    application.run_polling()


if __name__ == "__main__":
    main()
