from loguru import logger
import sys


def init_logger():
    # Очищаем все обработчики
    logger.remove()

    # Логи ошибок в отдельный файл
    logger.add(
        "logs/errors.log",
        rotation="10 MB",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}\n{exception}",
        backtrace=True,  # показывать полный traceback для ошибок
        diagnose=True    # показывать переменные в traceback
    )

    # Основные логи
    logger.add(
        "logs/app.log",
        rotation="50 MB",
        retention="3 months",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )

    # Дебаг логи (только для разработки)
    logger.add(
        "logs/debug.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        filter=lambda record: record["level"].name == "DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )

    # Вывод в консоль
    logger.add(
        sys.stderr,
        level="DEBUG",
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>"
    )