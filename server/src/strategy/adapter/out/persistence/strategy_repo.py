from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.strategy.adapter.out.persistence.strategy_mapper import StrategyMapper
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.strategy import StrategyDomainModel
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.strategy.adapter.out.persistence.strategy_entity import StrategyEntity
from src.strategy.domain.strategy_upsert_command import StrategyCreateCommand


class SqlAlchemyStrategyRepository(StrategyRepository):
    def __init__(self, session: Session, mapper: StrategyMapper, sa_repository: SqlalchemyRepository[StrategyEntity]):
        self.session = session
        self.mapper = mapper
        self.sa_repository = sa_repository

    def save(self, command: StrategyCreateCommand) -> StrategyDomainModel:
        entity = self.mapper.to_entity(command)
        self.sa_repository.save(entity)
        return entity

    def find_by_id(self, id: int) -> StrategyDomainModel | None:
        return self.sa_repository.find_by_id(id)

    def find_all(self) -> List[StrategyDomainModel]:
        return [self.mapper.to_model(entity) for entity in self.sa_repository.find_all()]

    def delete_by_id(self, id: int) -> int:
        return self.sa_repository.delete_by_id(id)

    def find_all_active(self) -> List[StrategyDomainModel]:
        with self.session as session:
            stmt = select(StrategyEntity).where(StrategyEntity.is_active == True)
            return [self.mapper.to_model(entity) for entity in session.scalars(stmt).all()]
