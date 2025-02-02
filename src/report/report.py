import yfinance as yf

from src.common.adapter.out.slack_noti_client import send_noti
from src.config import EXCEPTION_URL, FINANCE_REPORT_URL


def generate_report() -> str:
    # 현재 원-달러 환율
    exchange_rate_usd_krw = yf.Ticker("USDKRW=X").info.get("previousClose")

    return f"""
    원-달러 환율: {exchange_rate_usd_krw}
    """


# 리포트 발행
def publish_report():
    report = generate_report()
    send_noti(FINANCE_REPORT_URL, report)
