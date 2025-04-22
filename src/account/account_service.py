from typing import List, Optional
from account.account import Account
from account.account_mapper import AccountMapper
from common.exception import ExeptionType, InvestAppException
from db.database_session_manager import DBSessionManager
from db.sqlalchemy_repository import SqlalchemyRepository
from db.account_entity import AccountEntity


class AccountService:
    def __init__(self, account_mapper: AccountMapper, account_repository: SqlalchemyRepository[AccountEntity], session_manager: DBSessionManager):
        self.account_repository = account_repository
        self.account_mapper = account_mapper
        self.session_manager = session_manager

    def save(self, account: Account) -> Account:
        with self.session_manager.session() as session:
            entity = self.account_mapper.to_entity(account)
            saved_entity = self.account_repository.save(entity, session)
            return self.account_mapper.to_domain(saved_entity)

    def update(self, id: int, account: Account) -> Account:
        with self.session_manager.session() as session:
            found_entity: Optional[AccountEntity] = self.account_repository.find_by_id(id, session)
            if not found_entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)
            found_entity.update(self.account_mapper.to_entity(account))
            return self.account_mapper.to_domain(found_entity)

    def delete_by_id(self, id: int) -> int:
        with self.session_manager.session() as session:
            return self.account_repository.delete_by_id(id, session)

    def find_by_id(self, id: int) -> Account:
        with self.session_manager.session() as session:
            found_account = self.account_repository.find_by_id(id, session)
            if not found_account:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)
            return self.account_mapper.to_domain(found_account)

    def find_all(self) -> List[Account]:
        with self.session_manager.session() as session:
            entities = self.account_repository.find_all(session)
            return [self.account_mapper.to_domain(entity) for entity in entities]
