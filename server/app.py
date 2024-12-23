from src.common.domain.config import logger
from fastapi import FastAPI, Request
from src.account.adapter.in_comming.web import account_router
from src.strategy.adapter.in_comming.web import strategy
from fastapi.responses import JSONResponse
from src.common.domain.exception import InvestAppException
from src import scheduler

app = FastAPI(lifespan=scheduler.lifespan)

app.include_router(strategy.router)
app.include_router(account_router.router)


@app.exception_handler(InvestAppException)
async def handle(request: Request, exc: InvestAppException):
    logger.error(exc)
    return JSONResponse(status_code=exc.error_code, content=exc.message)


@app.exception_handler(AssertionError)
async def handle(request: Request, exc: AssertionError):
    logger.error(exc)
    return JSONResponse(status_code=400, content=str(exc))


@app.exception_handler(Exception)
async def handle(request: Request, exc: Exception):
    logger.error(exc)
    return JSONResponse(status_code=500, content=str(exc))


def create_app():
    return app
