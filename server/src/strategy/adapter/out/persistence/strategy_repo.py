from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.strategy import Strategy
from src.common.adapter.out.persistence.entity_mapper import EntityMapper
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity


class SqlAlchemyStrategyRepository(SqlalchemyRepository[StrategyEntity, Strategy], StrategyRepository):
    def __init__(self, session: Session, mapper: EntityMapper[StrategyEntity, Strategy]):
        super().__init__(session, mapper, StrategyEntity)

    def find_all_active(self) -> List[Strategy]:
        with self.session as session:
            stmt = select(self.entity_type).where(self.entity_type.is_active == True)
            return [self.mapper.to_model(entity) for entity in session.scalars(stmt).all()]
