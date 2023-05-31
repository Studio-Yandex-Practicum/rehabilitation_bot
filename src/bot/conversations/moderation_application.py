# import datetime
import json
import re
import string

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


forbidden_words = json.load(open('src/bot/forbidden_words.json'))
# forbidden_words = json.load(open('russian_words.json'))

# Подготовка данных
data = pd.read_csv("src/bot/conversations/spam.csv", encoding="utf-8")
data.drop(data.iloc[:, 2:5], inplace=True, axis=1)
data.rename(columns={"v1": "class", "v2": "text"}, inplace=True)

x = data["text"]
y = data["class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# Преобразование текста в числовые признаки
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(x_train)
# X_test_counts = vectorizer.transform(x_test)

# Обучение модели

nb = MultinomialNB().fit(X_train_counts, y_train)


async def chat_moderation(update, context):
    """Function for moderating the conversation"""
    # start_time = datetime.datetime.now()
    text = update.message.text
    text_no_digital = re.sub('[0-9]', '', text)
    if any(word.lower().translate(str.maketrans('', '', string.punctuation))
           in forbidden_words for word in text_no_digital.split(' ')):
        # end_time = datetime.datetime.now()
        # print(end_time-start_time)
        await update.effective_chat.send_message(
            text='Нецензурная лексика у нас под запретом!'
        )
        await update.message.delete()


async def chat_moderation_spam(update, context):
    message = update.message.text.lower()
    message = re.sub(r'\W', ' ', message)
    message = re.sub(r'\d+', '', message)
    text_counts = vectorizer.transform([message])
    if nb.predict(text_counts)[0] == 'spam':
        await update.effective_chat.send_message(
            text='Спам у нас под запретом!'
        )
        await update.message.delete()
