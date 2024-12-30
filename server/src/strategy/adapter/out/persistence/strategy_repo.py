from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.strategy.adapter.out.persistence.strategy_mapper import StrategyMapper
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.strategy import Strategy
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity


class SqlAlchemyStrategyRepository(StrategyRepository):
    def __init__(self, session: Session):
        self.session = session
        self.mapper = StrategyMapper()
        self.repository = SqlalchemyRepository(session, StrategyEntity)

    def save(self, strategy: Strategy) -> Strategy:
        entity = self.mapper.to_entity(strategy)
        saved_entity = self.repository.save(entity)
        return self.mapper.to_model(saved_entity)

    def update(self, id: int, strategy: Strategy) -> Strategy:
        found_strategy = self.find_by_id(id)
        found_strategy.update(strategy)
        return self.save(found_strategy)

    def find_by_id(self, id: int) -> Strategy:
        entity = self.repository.find_by_id(id)
        return self.mapper.to_model(entity)

    def delete_by_id(self, id: int) -> int:
        return self.repository.delete_by_id(id)

    def find_all(self) -> List[Strategy]:
        return [self.mapper.to_model(entity) for entity in self.repository.find_all()]

    def find_all_active(self) -> List[Strategy]:
        stmt = select(StrategyEntity).where(StrategyEntity.is_active == True)
        return [self.mapper.to_model(entity) for entity in self.session.scalars(stmt).all()]
