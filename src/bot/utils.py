import time

import emoji
from thefuzz import fuzz, process

from bot.constants.info.text import MAX_MESSAGES
from bot.obscene_words import obscene_words


pending_messages = {}
processed_users = {}


def increment_message_count(user_id, key):
    # if value in pending_messages:
    #     pending_messages[value] += 1
    # return pending_messages[value]
    processed_users[user_id][key] += 1
    print(processed_users)
    return processed_users[user_id][key]


def check_message_limit(message_count):
    return message_count >= MAX_MESSAGES


def send_message_to_the_conversation(chat, text):
    return chat.send_message(text=text)


def replace_emoji_with_symbols(current, previous):
    current_text = emoji.replace_emoji(current, replace="")
    previous_text = emoji.replace_emoji(previous, replace="")
    return current_text, previous_text


def find_obscene_words_in_a_message(message_text):
    # понадобится словарь исключений
    start = time.time()
    words = [word for word in message_text if len(word) > 2]
    best_matching = None
    for word in words:
        matching = process.extractOne(
            word, obscene_words, scorer=fuzz.ratio, score_cutoff=89
        )
        if matching is not None:
            best_matching = matching
            break
    stop = time.time()
    execution_time = stop - start
    return best_matching, execution_time


def set_dict_key_to_zero(user_id, key):
    processed_users[user_id][key] = 0


def initalize_user(user_id):
    user_data = {
        "sticker": 0,
        "emoji": 0,
    }
    processed_users[user_id] = user_data
