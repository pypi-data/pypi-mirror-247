import json

import numpy as np

from volstreet import config
import requests
from volstreet.config import logger


def notifier(message: str, webhook_url: str | list[str] = None, level: str = "INFO"):
    levels = ["INFO", "CRUCIAL", "ERROR"]
    if levels.index(level) < levels.index(config.NOTIFIER_LEVEL):
        return
    if isinstance(webhook_url, (list, tuple, set, np.ndarray)):
        notification_urls = [
            *filter(lambda x: x is not None and x is not False, webhook_url)
        ]
    elif isinstance(webhook_url, str) and webhook_url != "":
        notification_urls = [webhook_url]
    else:
        logger.info(message)
        return
    data = {"content": message}
    for url in notification_urls:
        try:
            requests.post(
                url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
        except requests.exceptions.SSLError as e:
            logger.error(
                f"Error while sending notification: {e}",
                exc_info=(type(e), e, e.__traceback__),
            )
    logger.info(message)
