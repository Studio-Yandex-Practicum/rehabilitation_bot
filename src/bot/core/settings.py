from dotenv import find_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False

    log_level: str = 'INFO'
    log_filename: str = 'app.log'
    log_format: str = '%(asctime)s, %(levelname)s, %(name)s, %(message)s'

    # smtp_server_port: int = 465
    # smtp_server_address: str = 'smtp.yandex.ru'
    # smtp_server_bot_email: str = ''
    # smtp_server_bot_password: str = ''

    # email_curator: str = ''

    database_engine: str
    obscene_file: str

    class Config:
        env_file = find_dotenv()
        env_file_encoding = 'utf-8'


settings = Settings()
