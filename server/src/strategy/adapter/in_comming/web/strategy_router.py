from fastapi import APIRouter
from src.containers import Container
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.application.service.strategy_service import StrategyService
from src.strategy.adapter.in_comming.web.model import StrategyUpsertReq

router = APIRouter(prefix="/strategies", tags=["strategy"])

container = Container.get_instance()
strategy_service: StrategyService = container.strategy_service()
strategy_repository: StrategyRepository = container.strategy_repository()


@router.post("/")
def save(req: StrategyUpsertReq):
    return strategy_repository.save(req.to_command())


@router.put("/{id}")
def update(id: int, req: StrategyUpsertReq):
    return strategy_repository.update(id, req.to_command())


@router.get("/")
def find_all():
    return strategy_repository.find_all()


@router.get("/{id}")
def get(id: int):
    return strategy_repository.find_by_id(id)


@router.delete("/{id}")
def delete(id: int):
    return strategy_repository.delete_by_id(id)


@router.post("/{id}/rebalance")
def rebalance(id: int):
    strategy = strategy_repository.find_by_id(id)
    return strategy_service.rebalance(strategy)
