from src.account.application.port.in_comming.account_validate_usecase import AccountValidateUsecase
from src.account.application.port.out.account_validate_port import AccountValidatePort
from src.account.domain.account_info import AccountInfo


class AccountValidateService(AccountValidateUsecase):
    def __init__(self, account_validate_port: AccountValidatePort):
        self.account_validate_port = account_validate_port

    def validate(self, account_info: AccountInfo) -> None:
        self.account_validate_port.validate(account_info)
