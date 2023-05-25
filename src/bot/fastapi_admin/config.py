from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Админ панель бота"
    app_description: str = "Панель управления позволяет добавлять\
                            вопросы для анкеты, \
                            получать информацию о пользователях и \
                            просматривать их ответы на вопросы из анкеты."
    database_url: str = "sqlite+aiosqlite:///questions.sqlite3"


settings = Settings()
