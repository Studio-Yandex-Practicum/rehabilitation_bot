import emoji
from thefuzz import process

from bot.constants.info.text import MAX_MESSAGES, REPLACEMENT_VALUE


pending_messages = {
    "sticker": 0,
}
obscene_words = ['мат', 'проверка', 'ругань']


def increment_message_count(value):
    if value in pending_messages:
        pending_messages[value] += 1
    return pending_messages[value]


def check_message_limit(message_count):
    return message_count >= MAX_MESSAGES


def send_message_to_the_conversation(chat, text):
    return chat.send_message(text=text)


def replace_emoji_with_symbols(current, previous):
    current_text = emoji.replace_emoji(current, replace=REPLACEMENT_VALUE)
    previous_text = emoji.replace_emoji(previous, replace=REPLACEMENT_VALUE)
    return current_text, previous_text


def find_obscene_words_in_a_message(message):
    # понадобится словарь исключений
    words = [word for word in message if len(word) > 2]
    best_matching = None
    for word in words:
        matching = process.extractOne(word, obscene_words, score_cutoff=70)
        if matching is not None:
            best_matching = matching
            break
    return best_matching


def set_dict_key_to_zero(key):
    pending_messages[key] = 0
