from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False


    log_level: str = 'INFO'
    log_filename: str = 'app.log'
    log_format: str = '%(asctime)s, %(levelname)s, %(name)s, %(message)s'

    smtp_server_port: int = 465
    smtp_server_address: str = 'smtp.yandex.ru'
    smtp_server_bot_email: str = ''
    smtp_server_bot_password: str = ''

    email_curator: str = ''


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings(telegram_token='6251635925:AAEsD35kpZWb6SWevOGHqVRLkVsW-9Vpkts')
