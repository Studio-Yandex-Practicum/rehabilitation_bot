from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.constants import callback, key, state
from bot.constants.state import MAIN_MENU
from bot.conversations import form_application, menu_application
from bot.conversations.main_application import greet_new_member, start, stop


form_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            form_application.start_form, pattern=fr"^{key.FORM}_\S*$"
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
                form_application.ask_data,
                pattern=fr"^{callback.ASK_DATA}_\S*$"
            ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, form_application.save_data
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(start, callback.BACK),
    ],
    allow_reentry=True,
)

greet_new_member_handler = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS,
    greet_new_member
)


main_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
    ],
    states={
        MAIN_MENU: [
            form_handler,
            CallbackQueryHandler(
                menu_application.menu, pattern=fr"^{key.MENU}_\S*$"
            ),
        ],
    },
    fallbacks=[
        CommandHandler('stop', stop)
    ],
    allow_reentry=True,
)
