from telegram.ext import (CommandHandler,
                          ConversationHandler)

from bot.constants.state import MAIN_MENU
from bot.conversations.main_application import main_menu, start

main_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
    ],
    states={
        MAIN_MENU: [
            # CallbackQueryHandler(
            # menu_application.menu, pattern=fr"^{key.MENU}_\S*$"
            # ),
            # uncomment after adding the menu manager
        ],
    },
    fallbacks=[
        CommandHandler('menu', main_menu)
    ],
    allow_reentry=True,
)
