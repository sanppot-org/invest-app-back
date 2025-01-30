from abc import ABC, abstractmethod

from src.account.application.port.out.account_repository import AccountRepository
from src.account.domain.account import Account
from src.account.domain.account_info import AccountInfo
from src.common.domain.exception import ExeptionType, InvestAppException
from src.account.adapter.out.kis.kis_account import KisRealAccount, KisVirtualAccount
from src.account.adapter.out.upbit.upbit_account import UpbitAccount


class AccountProvider(ABC):
    @abstractmethod
    def get_account(self, account_id: int) -> Account:
        pass


class RealAccountProvider(AccountProvider):
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def get_account(self, account_id: int) -> Account:
        account_info: AccountInfo = self.account_repository.find_by_id(account_id)

        if account_info.broker_type.is_kis() and not account_info.is_virtual:
            return KisRealAccount(account_info)

        if account_info.broker_type.is_kis() and account_info.is_virtual:
            return KisVirtualAccount(account_info)

        if account_info.broker_type.is_upbit():
            return UpbitAccount(account_info)

        raise InvestAppException(ExeptionType.INVALID_ACCOUNT_TYPE, account_info.broker_type)
