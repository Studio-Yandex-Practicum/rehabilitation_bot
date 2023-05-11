from telegram.ext import (CommandHandler,
                          ConversationHandler, CallbackQueryHandler)

from bot.constants.state import MAIN_MENU
from bot.conversations.main_application import start, main_menu


main_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],
        states={
            MAIN_MENU: [
            CallbackQueryHandler(
                menu_application.menu, pattern=fr"^{key.MENU}_\S*$"
            ),
            ],
        },
        fallbacks=[
            CommandHandler('start', start)
        ],
        allow_reentry=True,
    )
