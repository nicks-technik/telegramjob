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
        if Config.SPECIFIC_TEXT not in message:
            logger.debug(
                f"The text '{Config.SPECIFIC_TEXT}' is not in the message: {message}"
            )
            continue

        logger.debug(f"Processing message: {message}")
        message = message.replace("**", "")
        message = message.replace("https**://", "https://")

        if "https://" not in message:
            logger.debug("'https://' is in the message")
            continue

        task_match = re.search(
            r"(?:Mission Nr\.|Aufgaben Nr\.|{SPECIFIC_TEXT})\.?\s*(\d+)".format(
                SPECIFIC_TEXT=Config.SPECIFIC_TEXT
            ),
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
