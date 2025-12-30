import logging
import sys
from src.config import settings


def setup_logging():

    logger = logging.getLogger()

    log_level = getattr(logging, settings.log_level.upper())
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    logger.handlers = []
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Создаем глобальный логгер
logger = setup_logging()