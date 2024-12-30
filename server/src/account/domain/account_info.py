from dataclasses import dataclass
from typing import Optional
from src.common.domain.type import BrokerType
from src.account.domain.access_token import AccessToken


@dataclass
class AccountInfo:
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
