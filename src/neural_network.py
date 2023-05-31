import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


# from datetime import datetime


# Подготовка данных
data = pd.read_csv("src/bot/conversations/spam.csv", encoding="utf-8")
data.drop(data.iloc[:, 2:5], inplace=True, axis=1)
data.rename(columns={"v1": "class", "v2": "text"}, inplace=True)

x = data["text"]
y = data["class"]
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.20)

# Преобразование текста в числовые признаки
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(x_train)
# X_test_counts = vectorizer.transform(x_test)

# Обучение модели

nb = MultinomialNB().fit(X_train_counts, y_train)
# nb.fit(X_train_counts, y_train)


# Оценка точности модели на тестовой выборке
# accuracy = nb.score(X_test_counts, y_test)
# print('Accuracy:', accuracy)


def check_text(text):
    text_counts = vectorizer.transform(text)
    result = nb.predict_proba(text_counts)
    return result[0][1]


for i in range(10):
    message = input('Введите текст сообщения: ')
    answer = [message]
    print(check_text(answer))
