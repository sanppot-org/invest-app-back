from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from dependency_injector.wiring import inject, Provide
from src.account.adapter.out.kis import token_refresher
from src.common.adapter.out.google_sheet_client import update_upbit_balance
from src.containers import Container
from src.report.report import publish_report
from src.strategy.application.service.strategy_service import StrategyService


scheduler = BackgroundScheduler()
container = Container()


@inject
def trade_coin(strategy_service: StrategyService = Provide[Container.strategy_service]):
    strategy_id = 8  # TODO : 유연하게 설정하기
    strategy_service.trade(strategy_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container.wire(
        modules=[
            "src.strategy.application.service.strategy_service",
            "src.account.adapter.out.kis.token_refresher",
            "src.common.adapter.out.google_sheet_client",
            "src.strategy.adapter.in_comming.web.strategy_router",
            "src.account.adapter.in_comming.web.account_router",
        ]
    )

    token_refresher.refresh_kis_token()

    # 한투 토큰 갱신. 12시간마다 실행
    scheduler.add_job(token_refresher.refresh_kis_token, "cron", hour=9)
    # 경제 리포트 발행. 매일 오전 07:45마다 실행
    scheduler.add_job(publish_report, "cron", hour=7, minute=45)
    # 코인 자동 매매. 매시 10분마다 실행
    scheduler.add_job(trade_coin, "cron", minute=10)
    # 업비트 잔고 업데이트. 매일 오후 11시 50분에 실행
    scheduler.add_job(update_upbit_balance, "cron", hour=23, minute=50)

    scheduler.start()
    yield
    scheduler.shutdown()
    # 종료 시 정리
    container.unwire()
