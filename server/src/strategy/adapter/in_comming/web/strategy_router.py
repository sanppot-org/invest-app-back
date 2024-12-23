from fastapi import APIRouter
from src.containers import Container
from src.strategy.application.service.strategy_service import StrategyService
from src.strategy.adapter.in_comming.web.model import StrategyCreateReq

router = APIRouter(prefix="/strategies", tags=["strategy"])

container = Container.get_instance()
strategy_service: StrategyService = container.strategy_service()


@router.get("/")
def find_all():
    return strategy_service.find_all()


@router.post("/")
def save(req: StrategyCreateReq):
    return strategy_service.save(req.to_domain())


@router.put("/{id}")
def update(id: int, req: StrategyCreateReq):
    return strategy_service.update(id, req.to_domain())


@router.get("/{id}")
def get(id: int):
    return strategy_service.find_by_id(id)


@router.delete("/{id}")
def delete(id: int):
    return strategy_service.delete_by_id(id)


@router.post("/{id}/rebalance")
def rebalance(id: int):
    return strategy_service.rebalance(id)
