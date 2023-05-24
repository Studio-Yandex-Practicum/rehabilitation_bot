import json
import re
import string


forbidden_words = json.load(open('src/bot/forbidden_words.json'))


async def chat_moderation(update, context):
    """Function for moderating the conversation"""
    text = update.message.text
    text_no_digital = re.sub('[0-9]', '', text)
    if any(word.lower().translate(str.maketrans('', '', string.punctuation))
           in forbidden_words for word in text_no_digital.split(' ')):
        await update.effective_chat.send_message(
            text='Нецензурная лексика у нас под запретом!'
        )
        await update.message.delete()
