from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.strategy.domain.strategy_entity import StrategyEntity


class SqlAlchemyStrategyRepository:
    def __init__(self, session: Session, sa_repository: SqlalchemyRepository[StrategyEntity]):
        self.session = session
        self.sa_repository = sa_repository

    def save(self, entity: StrategyEntity) -> StrategyEntity:
        return self.sa_repository.save(entity)

    def find_by_id(self, id: int) -> StrategyEntity | None:
        return self.sa_repository.find_by_id(id)

    def find_all(self) -> List[StrategyEntity]:
        return self.sa_repository.find_all()

    def delete_by_id(self, id: int) -> int:
        return self.sa_repository.delete_by_id(id)

    def find_all_active(self) -> List[StrategyEntity]:
        with self.session as session:
            stmt = select(StrategyEntity).where(StrategyEntity.is_active == True)
            return list(session.scalars(stmt).all())
