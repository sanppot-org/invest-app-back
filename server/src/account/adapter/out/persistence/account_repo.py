from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.account.adapter.out.persistence.account_mapper import AccountMapper
from src.account.application.port.out.account_repository import AccountRepository
from src.account.domain.account_info import AccountInfo
from src.common.domain.type import BrokerType
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.account.adapter.out.persistence.account_entity import AccountEntity


class SqlAlchemyAccountRepository(AccountRepository):
    def __init__(self, session: Session, mapper: AccountMapper, sa_repository: SqlalchemyRepository[AccountEntity]):
        self.session = session
        self.mapper = mapper
        self.sa_repository = sa_repository

    def find_all(self, broker_type: BrokerType | None = None) -> List[AccountInfo]:
        stmt = select(AccountEntity)
        if broker_type is not None:
            stmt = stmt.where(AccountEntity.broker_type == broker_type)
        return [self.mapper.to_model(entity) for entity in self.session.scalars(stmt).all()]
