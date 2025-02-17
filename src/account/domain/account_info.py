from dataclasses import dataclass
from typing import Optional
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import BrokerType
from src.account.domain.access_token import AccessToken


@dataclass
class AccountInfo:
    """계좌 모델"""

    id: Optional[int]
    name: str
    app_key: str
    secret_key: str
    broker_type: BrokerType
    number: Optional[str]
    product_code: Optional[str]
    login_id: Optional[str]
    url_base: Optional[str]
    is_virtual: bool
    token: Optional[AccessToken]

    def __post_init__(self):
        """계좌 정보 검증"""
        if self.broker_type != BrokerType.KIS:
            return

        if self.login_id is None or self.url_base is None or self.product_code is None or self.number is None:
            raise InvestAppException(
                ExeptionType.INVALID_ACCOUNT_INFO,
                f"KIS 계좌는 다음 항목이 필수입니다. number, product_code, url_base, login_id",
            )

    def update(self, account_info: "AccountInfo"):
        self.name = account_info.name
        self.app_key = account_info.app_key
        self.secret_key = account_info.secret_key
        self.broker_type = account_info.broker_type
        self.login_id = account_info.login_id
        self.is_virtual = account_info.is_virtual
        self.number = account_info.number
        self.product_code = account_info.product_code
        self.url_base = account_info.url_base
