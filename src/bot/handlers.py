from telegram.ext import (CommandHandler,
                          ConversationHandler, MessageHandler, filters)
from src.bot.constants.state import MAIN_MENU
from src.bot.conversations.main_application import main_menu, start, greet_new_member

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

greet_new_member_handler = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS,
    greet_new_member
)
