import uvicorn
from fastapi import FastAPI
from app.routers import environment, strategy, account

app = FastAPI()

app.include_router(environment.router)
app.include_router(strategy.router)
app.include_router(account.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
