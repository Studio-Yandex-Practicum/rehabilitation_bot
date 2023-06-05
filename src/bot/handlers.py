from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants import callback, key, state
from bot.constants.state import MAIN_MENU
from bot.conversations import form_application
from bot.conversations.main_application import (
    greet_new_member,
    main_menu,
    manage_message_flooding,
    start,
    stop,
)


form_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            form_application.start_form, pattern=callback.START_FORM
        )
    ],
    states={
        state.FORM_SUBMISSION: [
            CallbackQueryHandler(
                form_application.edit_menu, pattern=callback.EDIT_MENU
            ),
            CallbackQueryHandler(
                form_application.send_data, pattern=callback.SEND_DATA
            ),
        ],
        state.FORM_INPUT: [
            CallbackQueryHandler(
                form_application.show_data, pattern=callback.SHOW_DATA
            ),
            CallbackQueryHandler(
                form_application.edit_data, pattern=fr"^{key.ASK}_\S*$"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, form_application.save_data
            ),
        ],
    },
    fallbacks=[
        CommandHandler('menu', main_menu)
    ],
    allow_reentry=True,
)


main_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
    ],
    states={
        MAIN_MENU: [
            form_handler,
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
    manage_message_flooding,
)
