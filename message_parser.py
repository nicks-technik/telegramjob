"""This module provides functions to parse Telegram messages and extract job-related information."""

import re

from config import Config
from logger_config import logger


def extract_jobs_from_messages(messages):
    """
    Extracts task numbers and YouTube links from a list of messages.

    Args:
        messages (list): A list of strings (messages).

    Returns:
        list: A list of dictionaries, where each dictionary contains
        the task number and youtube link,
        or an empty list if no data could be extracted.
    """
    logger.debug("Extracting info from messages...")
    extracted_data = []
    for message in messages:
        if not any(text in message for text in Config.SPECIFIC_TEXTS):
            logger.debug(f"None of the specific texts found in message: {message}")
            continue

        logger.debug(f"Processing message: {message}")
        message = message.replace("**", "")
        message = message.replace("https**://", "https://")

        if "https://" not in message:
            logger.debug("'https://' is in the message")
            continue

        specific_texts_pattern = "|".join(
            re.escape(text) for text in Config.SPECIFIC_TEXTS
        )
        task_match = re.search(
            rf"(?:{specific_texts_pattern})\.?\s*(\d+)",
            message,
        )
        link_match = re.search(r"(https?://[^\s]+)", message)

        if task_match and link_match:
            task_number = task_match.group(1)
            url = link_match.group(1)

            extracted_data.append(
                {
                    "task_number": task_number,
                    "url": url,
                }
            )
    return extracted_data
