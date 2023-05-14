from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler)

from bot.constants.state import MAIN_MENU
from bot.conversations.main_application import main_menu, start

main_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
    ],
    states={
        MAIN_MENU: [
            CallbackQueryHandler(
                # menu_application.menu, pattern=fr"^{key.MENU}_\S*$"
            ),
        ],
    },
    fallbacks=[
        CommandHandler('menu', main_menu)
    ],
    allow_reentry=True,
)

