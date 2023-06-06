from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False

    smtp_server_port: int = 465
    smtp_server_address: str = 'smtp.yandex.ru'
    smtp_server_bot_email: str = ''
    smtp_server_bot_password: str = ''

    email_curator: str = ''

    database_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
