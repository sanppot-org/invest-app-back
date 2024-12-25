from dataclasses import dataclass
from typing import Optional
from src.common.domain.base_domain_model import BaseDomainModel
from src.common.domain.type import BrokerType
from src.account.domain.access_token import AccessToken


@dataclass
class AccountInfo(BaseDomainModel):
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

    def get_update_fields(self) -> dict:
        return super().get_update_fields(exclude_keys=["token"])
