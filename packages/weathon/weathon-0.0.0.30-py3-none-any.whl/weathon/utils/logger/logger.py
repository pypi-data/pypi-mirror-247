import logging
from logging import Logger
from typing import Optional

init_loggers = {}

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(logger_name:str = None, log_file: Optional[str] = None, log_level: int = logging.DEBUG, file_mode: str = 'w'):
    """ Get logging logger
    Args:
        log_file: 日志文件,如果指定,文件处理器将会被加到logger对象中.
        log_level: Logging level.
        file_mode: 如果"log_file"不为空,指定打开日志文件的模式,默认为"w".
    """

    logger_name = __name__.split('.')[0] if not logger_name else logger_name
    logger: Logger = logging.getLogger(logger_name)

    if logger_name in init_loggers:
        add_file_handler_if_needed(logger, log_file, file_mode, log_level)
        return logger

    for handler in logger.root.handlers:
        if type(handler) is logging.StreamHandler:
            handler.setLevel(logging.ERROR)

    stream_handler = logging.StreamHandler()
    handlers = [stream_handler]

    for handler in handlers:
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        logger.addHandler(handler)

    logger.setLevel(logging.ERROR)

    init_loggers[logger_name] = True

    return logger


def add_file_handler_if_needed(logger, log_file, file_mode, log_level) -> None:
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return

    if log_file is not None:
        file_handler = logging.FileHandler(log_file, file_mode)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
