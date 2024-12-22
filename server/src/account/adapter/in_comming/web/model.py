from typing import Optional
from pydantic import BaseModel

from src.common.type import BrokerType
from src.account.application.port.out.account_repository import AccountInfo


class AccountCreateReq(BaseModel):
    name: str
    number: str
    product_code: str
    app_key: str
    secret_key: str
    url_base: str
    token: Optional[str] = None
    broker_type: BrokerType

    def to_domain(self) -> AccountInfo:
        return AccountInfo(
            name=self.name,
            number=self.number,
            product_code=self.product_code,
            app_key=self.app_key,
            secret_key=self.secret_key,
            url_base=self.url_base,
            token=self.token,
            broker_type=self.broker_type,
        )
