from account.account import Account


class VolStrategy:
    """
    변동성 돌파 전략
    """

    def __init__(self, account: Account):
        self.account = account
