from fastapi import FastAPI
from rest import environment, strategy, account


def create_app():
    app = FastAPI()

    app.include_router(environment.router)
    app.include_router(strategy.router)
    app.include_router(account.router)

    return app
