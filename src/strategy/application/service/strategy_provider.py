from src.account.application.service.account_provider import AccountProvider
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.strategy_info import StrategyInfo


class StrategyProvider:
    def __init__(self, strategy_repository: StrategyRepository, account_provider: AccountProvider):
        self.strategy_repository = strategy_repository
        self.account_provider = account_provider

    def get_strategy(self, strategy_id: int) -> StrategyInfo:
        strategy = self.strategy_repository.find_by_id(strategy_id)
        account = self.account_provider.get_account(strategy.account_id)
        return strategy
