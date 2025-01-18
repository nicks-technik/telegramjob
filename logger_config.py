import logging
import sys


def setup_logger(log_file="app.log", console_level=logging.WARNING):
    logger = logging.getLogger("main_logger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
        datefmt="%d.%m.%y %I:%M:%S",
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(console_level)
    stream_handler.setFormatter(formatter)

    # Add handlers if not already added
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    logger.propagate = False
    return logger


# Initialize the logger (executed once when this module is imported)
logger = setup_logger()
