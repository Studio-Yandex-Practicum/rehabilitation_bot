from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants.state import MAIN_MENU
from bot.conversations.main_application import (
    handle_all_messages,
    handle_messages_from_new_user,
    main_menu,
    start,
    welcome_new_user_in_group,
)


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


message_filter_handler = MessageHandler(
    filters.ALL & (~ filters.StatusUpdate.ALL), handle_all_messages)

welcome_filter_handler = MessageHandler(
    filters.TEXT & (filters.Entity("url") |
                    filters.Entity("text_link") |
                    filters.Entity("email") |
                    filters.Entity('mention')), handle_messages_from_new_user)

welcome_new_user_handler = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS,
    welcome_new_user_in_group
)
