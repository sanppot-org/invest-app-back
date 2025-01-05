import requests


def send_noti(url: str, msg: str):
    message = {"text": f"{msg}"}
    requests.post(url, json=message, headers={"Content-Type": "application/json"})
