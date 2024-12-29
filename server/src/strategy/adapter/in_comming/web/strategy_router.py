from fastapi import APIRouter
from src.containers import Container
from src.strategy.application.service.strategy_service import StrategyService
from src.strategy.adapter.in_comming.web.model import StrategyCreateReq

router = APIRouter(prefix="/strategies", tags=["strategy"])

container = Container.get_instance()
strategy_service: StrategyService = container.strategy_service()


@router.get("/", summary="전략 목록 조회")
def find_all():
    return strategy_service.find_all()


@router.post("/", summary="전략 생성")
def save(req: StrategyCreateReq):
    return strategy_service.save(req.to_domain())


@router.put("/{id}", summary="전략 수정")
def update(id: int, req: StrategyCreateReq):
    return strategy_service.update(id, req.to_domain())


@router.get("/{id}", summary="전략 상세 조회")
def get(id: int):
    return strategy_service.find_by_id(id)


@router.delete("/{id}", summary="전략 삭제")
def delete(id: int):
    return strategy_service.delete_by_id(id)


@router.post("/{id}/rebalance", summary="리밸런스")
def rebalance(id: int):
    strategy = strategy_service.find_by_id(id)
    return strategy_service.rebalance(strategy)
