import json
import re
import string

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

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


async def obscene_language(update, context):
    chat = update.effective_chat
    text = update.message.text
    text_no_digital = re.sub('[0-9]', '', text)
    if {i.lower().translate(str.maketrans(
            '', '', string.punctuation))
            for i in text_no_digital.split(' ')}.intersection(set(
            json.load(open('src/bot/forbidden_words.json')))) != set():
        await context.bot.send_message(
            chat_id=chat.id, text='Нецензурная лексика у нас под запретом!'
        )
        await update.message.delete()


swearing_words_handler = MessageHandler(
    filters.TEXT,
    obscene_language
)
