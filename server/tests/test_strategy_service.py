import copy
import pytest
from datetime import datetime
from typing import Dict, List

from src.common.application.port.out.time_holder import TimeHolder
from src.common.application.port.out.stock_market_port import StockMarketQueryPort
from src.containers import Container
from src.account.domain.account import Account
from src.account.application.service.account_provider import AccountProvider
from src.account.domain.holdings import HoldingsInfo
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.application.service.strategy_service import StrategyService
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy import Strategy
from src.common.domain.type import Market, TimeUnit
from src.account.adapter.out.persistence.account_entity import AccountEntity
from src.strategy.domain.interval import Interval


class FakeStockMarketClient(StockMarketQueryPort):
    def is_market_open(self, market: Market):
        pass

    def get_current_price(self, ticker: str) -> float:
        return 100


class FakeTimeHolder(TimeHolder):
    def get_now(self) -> datetime:
        return datetime(2024, 1, 1)


class FakeAccountProvider(AccountProvider):
    account: Account | None = None

    def get_account(self, account_id: int) -> Account:
        if FakeAccountProvider.account is None:
            FakeAccountProvider.account = FakeAccount(None)
        return FakeAccountProvider.account


class FakeAccount(Account):
    balance: float = 10_000
    holdings: Dict[str, HoldingsInfo] = {}

    def __init__(self, entity: AccountEntity | None):
        self.entity = entity

    def get_balance(self) -> float:
        return FakeAccount.balance

    def get_holdings(self) -> Dict[str, HoldingsInfo]:
        return FakeAccount.holdings

    def buy_market_order(self, ticker: str, amount: float) -> None:
        FakeAccount.balance -= 100 * amount

    def sell_market_order(self, ticker: str, amount: float) -> None:
        FakeAccount.balance += 100 * amount


class FakeStrategyRepository(StrategyRepository):
    id_counter: int = 1
    strategies: List[Strategy] = []

    def find_by_id(self, id: int) -> Strategy:
        return next((strategy for strategy in FakeStrategyRepository.strategies if strategy.id == id))

    def save(self, model: Strategy) -> Strategy:
        model.id = FakeStrategyRepository.id_counter
        FakeStrategyRepository.id_counter += 1
        FakeStrategyRepository.strategies.append(model)
        return model

    def delete_by_id(self, id: int) -> None:
        entity = next((strategy for strategy in FakeStrategyRepository.strategies if strategy.id == id), None)
        if entity is not None:
            FakeStrategyRepository.strategies.remove(entity)

    def find_all(self) -> List[Strategy]:
        return copy.deepcopy(FakeStrategyRepository.strategies)

    def update(self, id: int, dto: Strategy) -> Strategy:
        found_strategy = next((s for s in FakeStrategyRepository.strategies if s.id == id), None)
        if found_strategy is not None:
            FakeStrategyRepository.strategies.remove(found_strategy)
            FakeStrategyRepository.strategies.append(dto)
        return dto

    def find_all_active(self) -> List[Strategy]:
        return [s for s in FakeStrategyRepository.strategies if s.is_active]


@pytest.fixture
def container():
    container = Container()
    container.stock_market_query_port.override(FakeStockMarketClient())
    container.time_holder.override(FakeTimeHolder())
    container.account_provider.override(FakeAccountProvider())
    container.strategy_repository.override(FakeStrategyRepository())
    return container


@pytest.fixture
def strategy_service(container):
    return container.strategy_service()


@pytest.fixture
def test_strategy():
    return Strategy(
        id=None,
        name="정적 자산 배분",
        invest_rate=1,
        stocks={"spy": StockInfo(target_rate=1)},
        market=Market.US,
        interval=Interval(time_unit=TimeUnit.MONTH, values=[1]),
        last_run=None,
        account_id=10,
        is_active=True,
    )


class TestStrategyService:
    def test_rebalance_should_calculate_correct_quantities_and_update_balance(
        self, container: Container, strategy_service: StrategyService, test_strategy: Strategy
    ):
        """리밸런싱이 올바른 수량을 계산하고 잔고를 업데이트하는지 테스트"""
        # Given
        strategy_repo = container.strategy_repository()
        saved_strategy = strategy_repo.save(test_strategy)
        initial_balance = FakeAccount.balance

        # When
        strategy_service.rebalance(saved_strategy)

        # Then
        found_strategy = strategy_repo.find_by_id(saved_strategy.id)
        assert found_strategy.stocks["spy"].rebalance_qty == 100, "리밸런싱 후 SPY의 목표 수량이 100이어야 합니다"

        assert found_strategy.last_run.date() == datetime.now().date(), "마지막 실행 시간이 현재 날짜로 업데이트되어야 합니다"

        assert FakeAccount.balance == 0, f"모든 잔고({initial_balance})가 투자되어 0이 되어야 합니다"

    @pytest.fixture(autouse=True)
    def reset_fake_strategy_repo(self):
        FakeStrategyRepository.strategies = []
        FakeStrategyRepository.id_counter = 1
        yield

    @pytest.fixture(autouse=True)
    def reset_fake_account(self):
        """각 테스트 실행 전에 FakeAccount 상태를 초기화"""
        FakeAccount.balance = 10_000
        FakeAccount.holdings = {}
        yield
