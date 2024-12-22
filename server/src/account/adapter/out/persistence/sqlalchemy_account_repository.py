from typing import List
from pytest import Session
from sqlalchemy import select
from src.common.sqlalchmey.sqlalchemy_repository import SqlalchemyRepository
from src.account.adapter.out.persistence.account import AccountEntity
from src.account.application.port.out.account_repository import AccountInfo
from src.common.sqlalchmey.sqlalchmy_entity_mapper import SqlalchemyEntityMapper
from src.common.type import BrokerType


class SqlAlchemyAccountRepository(SqlalchemyRepository[AccountEntity, AccountInfo]):
    def __init__(self, session: Session, mapper: SqlalchemyEntityMapper[AccountEntity, AccountInfo]):
        super().__init__(session, mapper, AccountEntity)

    def find_all(self, broker_type: BrokerType = None) -> List[AccountInfo]:
        stmt = select(self.entity_type)
        if broker_type is not None:
            stmt = stmt.where(self.entity_type.broker_type == broker_type)
        return [self.mapper.to_model(entity) for entity in self.session.scalars(stmt).all()]

    def upsert_all(self, accounts_dtos: List[AccountInfo]) -> List[AccountInfo]:
        with self.session as session:
            [session.merge(self.mapper.to_entity(account_dto)) for account_dto in accounts_dtos]
            session.commit()
            return accounts_dtos
