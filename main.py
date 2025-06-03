from fastapi import FastAPI
import uvicorn

from src.common.infra.base_entity import BaseEntity
from src.account.web import account_router
from config import DB_URL
from src.config.containers import Container
from src.strategy.web import strategy_router

app = FastAPI()

# 의존성 주입
container = Container()
container.config.DB_URL.from_value(DB_URL)
container.init_resources()  # 리소스 초기화
container.wire(modules=[account_router, strategy_router])
BaseEntity.metadata.create_all(container.engine())  # 테이블 생성 코드 추가


app.include_router(account_router.router)
app.include_router(strategy_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
