from telegram.ext import (Application, CommandHandler,
                          ConversationHandler, CallbackQueryHandler)

from bot.core.settings import settings
from bot.conversations.main_application import start, MAIN_MENU, main_menu


def main() -> None:
    """Initialize a Telegram bot application with a main handler."""
    application = Application.builder().token(settings.telegram_token).build()
    main_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(main_menu, pattern=None)
        ],
        states={
            MAIN_MENU: [
                ...
            ],
        },
        fallbacks=[
            CommandHandler('start', start)
        ],
        allow_reentry=True,
    )
    application.add_handler(main_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
