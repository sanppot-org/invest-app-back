from typing import Optional

from src.account.access_token import AccessToken
from src.common.domain_model import DomainModel
from src.common.type import BrokerType


class Account(DomainModel):
    def __init__(
            self,
            name: str,
            app_key: str,
            secret_key: str,
            broker_type: BrokerType,
            id: Optional[int] = None,
            number: Optional[str] = None,
            product_code: Optional[str] = None,
            login_id: Optional[str] = None,
            url_base: Optional[str] = None,
            is_virtual: bool = False,
            token: Optional[AccessToken] = None,
    ):
        self.id = id
        self.name = name
        self.app_key = app_key
        self.secret_key = secret_key
        self.broker_type = broker_type
        self.number = number
        self.product_code = product_code
        self.login_id = login_id
        self.url_base = url_base
        self.is_virtual = is_virtual
        self.token = token

        self._validate()

    def update(self, account: "Account"):
        super().update(account)
        self._validate()

    def _validate(self):
        assert all([self.name, self.app_key, self.secret_key, self.broker_type]), "필수 필드가 누락되었습니다"

        if self.broker_type.is_kis():
            assert all([self.number, self.product_code, self.url_base, self.login_id]), "한투 계좌 필수 필드가 누락되었습니다"
