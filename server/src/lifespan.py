from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.containers import Container
from apscheduler.schedulers.background import BackgroundScheduler

from src.account.adapter.out.kis import token_refresher


scheduler = BackgroundScheduler()

container = Container.get_instance()
strategy_service = container.strategy_service()


@asynccontextmanager
async def lifespan(app: FastAPI):
    token_refresher.refresh_kis_token()
    scheduler.add_job(token_refresher.refresh_kis_token, "interval", hours=12)

    scheduler.start()
    yield
    scheduler.shutdown()
