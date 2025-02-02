from contextlib import asynccontextmanager

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from src.account.adapter.out.kis import token_refresher
from src.containers import Container
from src.report.report import publish_report

scheduler = BackgroundScheduler()
container = Container.get_instance()
strategy_service = container.strategy_service()


def trade_coin():
    strategy_id = 3
    strategy_service.trade(strategy_id)


@asynccontextmanager
async def lifespan(app: FastAPI):
    token_refresher.refresh_kis_token()

    scheduler.add_job(token_refresher.refresh_kis_token, "interval", hours=12)
    scheduler.add_job(publish_report, "cron", hour=7, minute=45)  # 매일 오전 07:45마다 실행

    scheduler.add_job(trade_coin, "cron", minute="10")  # 매시 10분마다 실행

    scheduler.start()
    yield
    scheduler.shutdown()
