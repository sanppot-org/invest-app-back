from typing import List
from sqlalchemy import select
from src.account.adapter.out.persistence.account_mapper import AccountMapper
from src.account.application.port.out.account_repository import AccountRepository
from src.account.domain.account_info import AccountInfo
from src.common.adapter.out.persistence.engine import session_scope
from src.common.adapter.out.persistence.sqlalchemy_repository import SqlalchemyRepository
from src.common.domain.type import BrokerType
from src.account.adapter.out.persistence.account_entity import AccountEntity


class SqlAlchemyAccountRepository(AccountRepository):
    def __init__(self):
        self.mapper = AccountMapper()
        self.repository = SqlalchemyRepository(AccountEntity)

    def save(self, account_info: AccountInfo) -> AccountInfo:
        entity = self.mapper.to_entity(account_info)
        saved_entity = self.repository.save(entity)
        return self.mapper.to_model(saved_entity)

    def update(self, id: int, account_info: AccountInfo) -> AccountInfo:
        found_account = self.find_by_id(id)
        found_account.update(account_info)
        return self.save(found_account)

    def delete_by_id(self, id: int) -> int:
        return self.repository.delete_by_id(id)

    def find_by_id(self, id: int) -> AccountInfo:
        entity = self.repository.find_by_id(id)
        return self.mapper.to_model(entity)

    def find_all(self, broker_type: BrokerType | None = None) -> List[AccountInfo]:
        stmt = select(AccountEntity)
        if broker_type is not None:
            stmt = stmt.where(AccountEntity.broker_type == broker_type)
        with session_scope() as session:
            return [self.mapper.to_model(entity) for entity in session.scalars(stmt).all()]

    def upsert_all(self, accounts_dtos: List[AccountInfo]) -> List[AccountInfo]:
        with session_scope() as session:
            [session.merge(self.mapper.to_entity(account_dto)) for account_dto in accounts_dtos]
            session.commit()
        return accounts_dtos
