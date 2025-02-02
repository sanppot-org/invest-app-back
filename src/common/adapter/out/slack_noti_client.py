import requests
from src.common.domain.logging_config import logger
from src.config import EXCEPTION_URL, INVEST_APP_DEBUG_URL


def send_noti(url: str, msg: str):
    message = {"text": f"{msg}"}
    requests.post(url, json=message, headers={"Content-Type": "application/json"})


def send_debug_noti(msg: str):
    logger.debug(msg)
    send_noti(INVEST_APP_DEBUG_URL, msg)


def send_exception(msg: str):
    logger.error(msg)
    send_noti(EXCEPTION_URL, msg)
