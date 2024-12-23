from abc import ABC, abstractmethod

from src.account.domain.account_info import AccountInfo


class AccountValidatePort(ABC):
    @abstractmethod
    def validate(self, account_info: AccountInfo) -> None:
        pass
