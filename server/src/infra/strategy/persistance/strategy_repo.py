from sqlalchemy.orm import Session
from src.domain.strategy.strategy import Strategy
from src.common.adapter.out.persistence.entity_mapper import EntityMapper
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.infra.strategy.persistance.strategy import StrategyEntity


class SqlAlchemyStrategyRepository(SqlalchemyRepository[StrategyEntity, Strategy]):
    def __init__(self, session: Session, mapper: EntityMapper[StrategyEntity, Strategy]):
        super().__init__(session, mapper, StrategyEntity)
