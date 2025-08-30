import re

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
    logger.debug("In Extracting info from messages...")
    extracted_data = []
    for message in messages:
        if "Tätigkeit" not in message:
            logger.debug(f"The text 'Tätigkeit' is not in the {message}")
            continue

        logger.info(msg=f"==Actual Message: {message}")
        message = message.replace("**", "")
        message = message.replace("https**://", "https://")

        if "https://www.otto.de" not in message and "https://" not in message:
            logger.info(f"Neither 'https://www.otto.de' nor 'https://' is in the message")
            continue

        task_match = re.search(
            r"(?:Mission Nr\.|Aufgaben Nr\.|Tätigkeit)\.?\s*(\d+)", message
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
