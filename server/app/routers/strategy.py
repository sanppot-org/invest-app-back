from fastapi import APIRouter
from infra import strategy_repo
from infra.schema import Strategy
from web.strategy_req import StrategyReq

router = APIRouter(prefix="/strategies", tags=["strategy"])


@router.get("/")
def find_all_strategy():
    return strategy_repo.find_all()


@router.post("/")
def create_strategy(req: StrategyReq):
    return strategy_repo.save(Strategy(name=req.name))
