from src.account.application.port.out.account_repository import AccountInfo, AccountRepository


class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def save(self, account: AccountInfo):
        self.account_repository.save(account)

    def update(self, id: int, account: AccountInfo):
        self.account_repository.update(id, account)

    def find_all(self):
        return self.account_repository.find_all()

    def find_by_id(self, id: int):
        return self.account_repository.find_by_id(id)

    def delete_by_id(self, id: int):
        return self.account_repository.delete_by_id(id)

    def get_balance(self, id: int):
        return self.account_repository.get_balance(id)

    def get_holdings(self, id: int):
        return self.account_repository.get_holdings(id)
