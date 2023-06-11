import logging.config
from pathlib import Path

from src.bot.core.settings import settings


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / 'logs'
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_PATH / settings.log_filename

DEFAULT_LOGGING = {
    'version': 1,
    'disable_exising_loggers': False,
    'formatters': {
        'default': {
            'format': settings.log_format,
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            'level': settings.log_level,
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': LOG_PATH,
            'when': 'D',
            'interval': 1,
            'backupCount': 60,
            'level': settings.log_level,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'level': settings.log_level,
            'propagate': True,
            'handlers': ['default', 'file'],
        },
    },
}
logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__name__)
