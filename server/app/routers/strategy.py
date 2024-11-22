from fastapi import APIRouter
from infra import strategy_repo
from infra.schema import Strategy
from web.strategy_req import StrategyCreateReq, StrategyUpdateReq

router = APIRouter(prefix="/strategies", tags=["strategy"])


@router.get("/")
def find_all():
    return strategy_repo.find_all()


@router.post("/")
def save(req: StrategyCreateReq):
    return strategy_repo.save(Strategy(name=req.name))


@router.put("/{id}")
def update(id: int, req: StrategyUpdateReq):
    return strategy_repo.update(
        id, Strategy(name=req.name, invest_rate=req.invest_rate)
    )


@router.get("/{id}")
def get(id: int):
    return strategy_repo.get(id)


@router.delete("/{id}")
def delete(id: int):
    return strategy_repo.delete(id)
