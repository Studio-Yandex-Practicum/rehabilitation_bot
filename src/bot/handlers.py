from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants.state import MAIN_MENU
from bot.conversations.main_application import (
    greet_new_member,
    handle_all_messages,
    main_menu,
    start,
    stop,
)


main_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
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
        CommandHandler("menu", main_menu),
        CommandHandler("stop", stop),
    ],
    allow_reentry=True,
)

greet_new_member_handler = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member
)

message_filter_handler = MessageHandler(
    filters.TEXT | filters.Sticker.ALL & (~filters.StatusUpdate.ALL),
    handle_all_messages,
)
