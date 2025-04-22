from fastapi import FastAPI
import uvicorn

from .containers import Container
from .web import my_router

app = FastAPI()

# 의존성 주입
container = Container()
container.wire(modules=[my_router])

app.include_router(my_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
