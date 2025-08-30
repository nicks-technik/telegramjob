"""
This module configures the logging system for the application.
"""

import logging
import sys
import coloredlogs


def setup_logger(log_file="app.log", console_level=logging.WARNING):
    """
    Set up the logger for the application.
    """
    _logger = logging.getLogger("main_logger")
    _logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s-%(levelname)s-%(filename)s-%(funcName)s-%(lineno)d- %(message)s",
        datefmt="%d.%m.%y %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_formatter = coloredlogs.ColoredFormatter(
        fmt="%(asctime)s-%(levelname)s-%(filename)s-%(funcName)s-%(lineno)d- %(message)s",
        datefmt="%d.%m.%y %H:%M:%S",
        level_styles={
            'debug': {'color': 'green'},
            'info': {'color': 'cyan'},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True},
        },
        field_styles={
            'asctime': {'color': 'white'},
        }
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers if not already added
    if not _logger.handlers:
        _logger.addHandler(file_handler)
        _logger.addHandler(console_handler)

    _logger.propagate = False
    return _logger


# Initialize the logger (executed once when this module is imported)
logger = setup_logger(console_level=logging.INFO)