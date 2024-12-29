from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.account.domain.account_info import AccountInfo
from src.common.domain.type import BrokerType
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.account.adapter.out.persistence.account_entity import AccountEntity


class SqlAlchemyAccountRepository:
    def __init__(self, session: Session, sa_repository: SqlalchemyRepository[AccountEntity]):
        self.session = session
        self.sa_repository = sa_repository

    def save(self, entity: AccountEntity) -> AccountEntity:
        return self.sa_repository.save(entity)

    def update(self, entity: AccountEntity) -> AccountEntity:
        return self.sa_repository.update(entity)

    def find_by_id(self, id: int) -> AccountEntity | None:
        return self.sa_repository.find_by_id(id)

    def delete_by_id(self, id: int) -> None:
        self.sa_repository.delete_by_id(id)

    def find_all(self, broker_type: BrokerType | None = None) -> List[AccountEntity]:
        with self.session as session:
            stmt = select(AccountEntity)
            if broker_type is not None:
                stmt = stmt.where(AccountEntity.broker_type == broker_type)
            return list(session.scalars(stmt).all())
