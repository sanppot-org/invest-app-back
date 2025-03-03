from typing import List
from sqlalchemy import select
from src.common.adapter.out.persistence.engine import session_scope
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.strategy.adapter.out.persistence.strategy_mapper import StrategyMapper
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.strategy import Strategy
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity


class SqlAlchemyStrategyRepository(StrategyRepository):
    def __init__(self):
        self.mapper = StrategyMapper()
        self.repository = SqlalchemyRepository(StrategyEntity)

    def save(self, strategy: Strategy) -> Strategy:
        with session_scope() as session:
            entity = self.mapper.to_entity(strategy)
            saved_entity = self.repository.save(entity, session)
            return self.mapper.to_model(saved_entity)

    def update(self, id: int, strategy: Strategy) -> Strategy:
        found_strategy = self.find_by_id(id)
        found_strategy.update(strategy)
        return self.save(found_strategy)

    def find_by_id(self, id: int) -> Strategy:
        with session_scope() as session:
            entity = self.repository.find_by_id(id, session)
            return self.mapper.to_model(entity)

    def delete_by_id(self, id: int) -> int:
        return self.repository.delete_by_id(id)

    def find_all(self) -> List[Strategy]:
        with session_scope() as session:
            return list(map(self.mapper.to_model, self.repository.find_all(session)))

    def find_all_active(self) -> List[Strategy]:
        with session_scope() as session:
            stmt = select(StrategyEntity).where(StrategyEntity.is_active == True)
            return list(map(self.mapper.to_model, session.scalars(stmt).all()))

    def upsert_all(self, strategies: List[Strategy]) -> List[Strategy]:
        return []
