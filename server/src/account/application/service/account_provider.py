from abc import ABC, abstractmethod


from src.account.domain.account import Account
from src.account.domain.account_info import AccountInfo
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.application.port.out.repository import Repository
from src.common.domain.type import BrokerType
from src.account.adapter.out.kis.kis_account import KisRealAccount, KisVirtualAccount
from src.account.adapter.out.upbit.upbit_account import UpbitAccount


class AccountProvider(ABC):
    @abstractmethod
    def get_account(self, account_id: int) -> Account:
        pass


class RealAccountProvider(AccountProvider):
    def __init__(self, account_repository: Repository[AccountInfo]):
        self.account_repository = account_repository

    def get_account(self, account_id: int) -> Account:
        account_dto: AccountInfo = self.account_repository.find_by_id(account_id)

        if account_dto.broker_type == BrokerType.KIS and not account_dto.is_virtual:
            return KisRealAccount(account_dto)

        if account_dto.broker_type == BrokerType.KIS and account_dto.is_virtual:
            return KisVirtualAccount(account_dto)

        if account_dto.broker_type == BrokerType.UPBIT:
            return UpbitAccount(account_dto)

        raise InvestAppException(ExeptionType.INVALID_ACCOUNT_TYPE, account_dto.broker_type)
