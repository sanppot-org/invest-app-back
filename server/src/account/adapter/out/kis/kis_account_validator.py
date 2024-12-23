from src.account.application.port.out.account_validate_port import AccountValidatePort
from src.account.domain.account_info import AccountInfo
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import BrokerType


class KisAccountValidator(AccountValidatePort):
    def validate(self, account_info: AccountInfo) -> None:
        if account_info.broker_type != BrokerType.KIS:
            return

        if account_info.login_id is None or account_info.url_base is None or account_info.product_code is None or account_info.number is None:
            raise InvestAppException(
                ExeptionType.INVALID_ACCOUNT_INFO,
                f"login_id: {account_info.login_id}, url_base: {account_info.url_base}, product_code: {account_info.product_code}, number: {account_info.number}",
            )
