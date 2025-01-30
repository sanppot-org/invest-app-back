import traceback
from src.common.adapter.in_comming import stock_market_router
from src.common.domain.config import logger
from fastapi import FastAPI, Request
from src.account.adapter.in_comming.web import account_router
from src.report.report import send_exception
from src.strategy.adapter.in_comming.web import strategy_router
from fastapi.responses import JSONResponse
from src.common.domain.exception import InvestAppException
from src.lifespan import lifespan


def create_app():
    app = FastAPI(lifespan=lifespan)

    app.include_router(strategy_router.router)
    app.include_router(account_router.router)
    app.include_router(stock_market_router.router)

    @app.exception_handler(InvestAppException)
    async def handle_invest_app_exception(request: Request, exc: InvestAppException):
        logger.error(exc)
        return JSONResponse(status_code=exc.error_code, content=exc.message)

    @app.exception_handler(AssertionError)
    async def handle_assertion_error(request: Request, exc: AssertionError):
        logger.error(exc)
        return JSONResponse(status_code=400, content=str(exc))

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception):
        logger.error(exc)
        send_exception(traceback.format_exc())
        return JSONResponse(status_code=500, content=str(exc))

    return app
