from fastapi import APIRouter
from src.containers import Container
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.application.service.strategy_service import StrategyService
from src.strategy.adapter.in_comming.web.model import StrategyCreateReq

router = APIRouter(prefix="/strategies", tags=["strategy"])

container = Container.get_instance()
strategy_service: StrategyService = container.strategy_service()
strategy_repo: StrategyRepository = container.strategy_repository()


@router.get("/", summary="전략 목록 조회")
def find_all():
    return strategy_repo.find_all()


@router.post("/", summary="전략 생성")
def save(req: StrategyCreateReq):
    model = req.to_domain()
    model.validate_portfolio_rate()
    return strategy_repo.save(model)


@router.put("/{id}", summary="전략 수정")
def update(id: int, req: StrategyCreateReq):
    model = req.to_domain()
    model.validate_portfolio_rate()
    return strategy_repo.update(id, model)


@router.get("/{id}", summary="전략 상세 조회")
def get(id: int):
    return strategy_repo.find_by_id(id)


@router.delete("/{id}", summary="전략 삭제")
def delete(id: int):
    return strategy_repo.delete_by_id(id)


@router.post("/{id}/rebalance", summary="리밸런스")
def rebalance(id: int, is_force: bool = False):
    strategy = strategy_repo.find_by_id(id)
    return strategy_service.rebalance(strategy, is_force)
