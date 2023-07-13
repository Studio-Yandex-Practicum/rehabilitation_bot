from telegram.ext import Application
from bot.core.logger import logger
from bot.core.settings import settings
from bot.handlers import (
    greet_new_member_handler,
    main_handler,
    moderate_conversation_handler,
)
from bot.utils import update_obscene_words_db_table


async def post_init(application: Application) -> None:
    """
    Uploads data to database after application has initialized.
    """
    await update_obscene_words_db_table()
    logger.info("Data uploaded: obscene words database updated.")


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = (
        Application.builder()
        .token(settings.telegram_token)
        .post_init(post_init)
        .build()
    )
    application.add_handlers(
        [
            main_handler,
            greet_new_member_handler,
            moderate_conversation_handler,
        ]
    )
    application.run_polling()


if __name__ == "__main__":
    main()
