from typing import Optional
from pydantic import BaseModel
from src.account.domain.account_info import AccountInfo
from src.common.domain.type import BrokerType


class AccountCreateReq(BaseModel):
    name: str
    app_key: str
    secret_key: str
    broker_type: BrokerType
    login_id: Optional[str] = None
    is_virtual: Optional[bool] = False
    number: Optional[str] = None
    product_code: Optional[str] = None
    url_base: Optional[str] = None
    token: Optional[str] = None

    def to_domain(self) -> AccountInfo:
        return AccountInfo(
            id=None,
            name=self.name,
            login_id=self.login_id,
            number=self.number,
            product_code=self.product_code,
            app_key=self.app_key,
            secret_key=self.secret_key,
            url_base=self.url_base,
            token=self.token,
            broker_type=self.broker_type,
            is_virtual=self.is_virtual,
        )
