from abc import ABC, abstractmethod

from src.account.domain.account_info import AccountInfo


class AccountValidateUsecase(ABC):
    @abstractmethod
    def validate(self, account_info: AccountInfo) -> None:
        pass
