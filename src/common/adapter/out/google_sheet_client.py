import gspread

from dependency_injector.wiring import inject, Provide
from src.account.application.service.account_provider import AccountProvider
from src.common.adapter.out.slack_noti_client import send_debug_noti
from src.config import SPREADSHEET_URL
from src.containers import Container

JSON_FILE_PATH = "config-module/auto-trade-google-key.json"
gc = gspread.service_account(JSON_FILE_PATH)
doc = gc.open_by_url(SPREADSHEET_URL)
dashboard = doc.worksheet("대시보드")


@inject
def update_upbit_balance(account_provider: AccountProvider = Provide[Container.account_provider]):
    account = account_provider.get_account(3)
    upbit_balance = account.get_balance()
    dashboard.update_acell(
        "I7",
        upbit_balance,
    )
    send_debug_noti(f"업비트 잔고 업데이트: {upbit_balance}")
