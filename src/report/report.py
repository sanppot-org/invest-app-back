import yaml
import yfinance as yf

from src.common.adapter.out.slack_noti_client import send_noti


def generate_report() -> str:
    # 현재 원-달러 환율
    exchange_rate_usd_krw = yf.Ticker("USDKRW=X").info.get("previousClose")

    return f"""
    원-달러 환율: {exchange_rate_usd_krw}
    """


# url 가져오기
with open("config-module/noti-url.yml", encoding="UTF-8") as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


# 리포트 발행
def publish_report():
    report = generate_report()
    send_noti(_cfg["finance-report"], report)


def send_exception(msg: str):
    send_noti(_cfg["exception"], msg)
