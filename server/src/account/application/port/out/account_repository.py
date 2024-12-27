from abc import ABC, abstractmethod
from typing import List
from src.common.application.port.out.repository import Repository
from src.account.domain.account_info import AccountInfo
from src.account.domain.account_create_command import AccountCreateCommand
from src.common.domain.type import BrokerType


class AccountRepository(Repository[AccountCreateCommand, AccountInfo], ABC):
    @abstractmethod
    def find_all(self, broker_type: BrokerType | None = None) -> List[AccountInfo]:
        pass
