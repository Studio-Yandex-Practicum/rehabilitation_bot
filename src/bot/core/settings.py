from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_token: str
    debug: bool = False

    log_level: str = 'INFO'
    log_filename: str = 'app.log'
    log_format: str = '%(asctime)s, %(levelname)s, %(name)s, %(message)s'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
