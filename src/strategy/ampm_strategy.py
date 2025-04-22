from src.account.account_operator import AccountOperator


class AmpmStrategy:
    """
    오전 오후 전략
    """

    def __init__(self, account_operator: AccountOperator):
        self.account_operator = account_operator
