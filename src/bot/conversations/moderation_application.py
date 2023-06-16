import re
import string
from datetime import datetime, timedelta

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from telegram import Update
from telegram.ext import ContextTypes

from bot.constants.info.text import FLOOD_MESSAGE
from bot.core.settings import settings
from bot.utils import (
    check_message_limit,
    create_community_member,
    fuzzy_string_matching,
    get_community_member_from_db,
    get_obscene_words_from_db,
    preformatted_text,
    update_community_member_data,
)


# Подготовка данных
data = pd.read_csv(settings.spam_file, encoding="utf-8")
data.drop(data.iloc[:, 2:5], inplace=True, axis=1)
data.rename(columns={"v1": "class", "v2": "text"}, inplace=True)
x = data["text"]
y = data["class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# Преобразование текста в числовые признаки
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(x_train)

# Обучение модели

nb = MultinomialNB().fit(X_train_counts, y_train)


async def chat_moderation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function for moderating the conversation"""
    text = update.message.text
    text_no_digital = re.sub("[0-9]", "", text)
    forbidden_words = await get_obscene_words_from_db()
    if any(
        word.lower().translate(str.maketrans("", "", string.punctuation))
        in forbidden_words
        for word in text_no_digital.split(" ")
    ):
        await update.effective_chat.send_message(
            text="Нецензурная лексика у нас под запретом!"
        )
        await update.message.delete()


async def chat_moderation_spam(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    message = update.message.text.lower()
    message = re.sub(r"\W", " ", message)
    message = re.sub(r"\d+", "", message)
    text_counts = vectorizer.transform([message])
    if nb.predict(text_counts)[0] == "spam":
        await update.effective_chat.send_message(
            text="Спам у нас под запретом!"
        )
        await update.message.delete()


async def manage_message_flooding(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Monitoring and managing message flooding and sticker usage by comparing
    text similarity and tracking the number of stickers sent by each user.
    """
    current_message = update.message
    user_id = current_message.from_user.id
    current_time = datetime.now().replace(microsecond=0)
    user_first_name = current_message.from_user.first_name

    community_member = await get_community_member_from_db(user_id)

    if not community_member:
        await create_community_member(user_id, current_message)
        return

    last_message = community_member.last_message

    if last_message.sticker and current_message.sticker:
        previous_time = last_message.timestamp
        elapsed_time = current_time - previous_time
        time_diff = elapsed_time < timedelta(seconds=30)

        message_count = await update_community_member_data(
            community_member, current_message, time_diff
        )

        if check_message_limit(message_count):
            await current_message.reply_text(
                text=FLOOD_MESSAGE.format(user_first_name)
            )
        return

    if last_message.text and current_message.text:
        current_text, previous_text = preformatted_text(
            current_message.text, last_message.text
        )

        if fuzzy_string_matching(current_text, previous_text):
            await current_message.reply_text(
                text=FLOOD_MESSAGE.format(user_first_name)
            )

    await update_community_member_data(community_member, current_message)
