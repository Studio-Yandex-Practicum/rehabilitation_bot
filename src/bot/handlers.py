
from telegram.ext import (CommandHandler, ConversationHandler, MessageHandler,
                          filters)

from bot.constants.state import MAIN_MENU
from bot.conversations.main_application import main_menu, start, stop
from bot.conversations.moderation_application import (chat_moderation,
                                                      chat_moderation_spam)


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
        CommandHandler('menu', main_menu),
        CommandHandler('stop', stop)
    ],
    allow_reentry=True,
)


moderation_handler = MessageHandler(
    filters.TEXT,
    chat_moderation
)

moderation_spam_handler = MessageHandler(
    filters.TEXT,
    chat_moderation_spam
)
