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
from src.strategy.application.service.strategy_service import StrategyService
from src.common.domain.type import Market
from src.account.adapter.out.persistence.account_entity import AccountEntity


class FakeStockMarketClient(StockMarketQueryPort):
    def is_market_open(self, market: Market):
        pass

    def get_current_price(self, ticker: str) -> float:
        return 100


class FakeTimeHolder(TimeHolder):
    def get_now(self) -> datetime:
        return datetime(2024, 1, 1)


class FakeAccountProvider(AccountProvider):
    account: Account = None

    def get_account(self, account_id: int) -> Account:
        if FakeAccountProvider.account is None:
            FakeAccountProvider.account = FakeAccount(None)
        return FakeAccountProvider.account


class FakeAccount(Account):
    balance: float = 10_000
    holdings: Dict[str, HoldingsInfo] = {}

    def __init__(self, entity: AccountEntity):
        self.entity = entity

    def get_balance(self) -> float:
        return FakeAccount.balance

    def get_holdings(self) -> Dict[str, HoldingsInfo]:
        return FakeAccount.holdings

    def buy_market_order(self, ticker: str, amount: float) -> None:
        FakeAccount.balance -= 100 * amount

    def sell_market_order(self, ticker: str, amount: float) -> None:
        FakeAccount.balance += 100 * amount


class FakeStrategyRepository(Repository[StrategyCreateCommand, StrategyDomainModel]):
    id_counter: int = 1
    strategies: List[StrategyDomainModel] = []
    mapper: StrategyMapper = StrategyMapper()

    def find_by_id(self, id: int) -> StrategyDomainModel | None:
        return next((strategy for strategy in FakeStrategyRepository.strategies if strategy.id == id), None)

    def save(self, command: StrategyCreateCommand) -> StrategyDomainModel:
        entity = self.mapper.command_to_entity(command)
        domail_model = self.mapper.entity_to_model(entity)
        domail_model.id = FakeStrategyRepository.id_counter
        FakeStrategyRepository.id_counter += 1
        FakeStrategyRepository.strategies.append(domail_model)
        return domail_model

    def delete_by_id(self, id: int) -> int:
        entity = next((strategy for strategy in FakeStrategyRepository.strategies if strategy.id == id), None)
        if entity is not None:
            FakeStrategyRepository.strategies.remove(entity)
        return id

    def find_all(self) -> List[StrategyDomainModel]:
        return copy.deepcopy(FakeStrategyRepository.strategies)

    def update(self, model: StrategyDomainModel) -> StrategyDomainModel:
        found_strategy = next((s for s in FakeStrategyRepository.strategies if s.id == model.id), None)
        entity = self.mapper.model_to_entity(model)
        if found_strategy is not None:
            FakeStrategyRepository.strategies.remove(found_strategy)
            FakeStrategyRepository.strategies.append(entity)
        return entity


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
def strategy_repo() -> FakeStrategyRepository:
    return FakeStrategyRepository()


class TestStrategyService:
    def test_rebalance_should_calculate_correct_quantities_and_update_balance(
        self,
        container: Container,
        strategy_service: StrategyService,
    ):
        """리밸런싱이 올바른 수량을 계산하고 잔고를 업데이트하는지 테스트"""
        # Given
        strategy_repo = container.strategy_repository()
        saved_strategy = strategy_repo.save(strategy_create_command)
        initial_balance = FakeAccount.balance

        # When
        strategy_service.rebalance(saved_strategy)

        # Then
        found_strategy = strategy_repo.find_by_id(saved_strategy.id)
        assert found_strategy.stocks["spy"].rebalance_qty == 100, "리밸런싱 후 SPY의 목표 수량이 100이어야 합니다"

        assert found_strategy.last_run.date() == datetime.now().date(), "마지막 실행 시간이 현재 날짜로 업데이트되어야 합니다"

        assert FakeAccount.balance == 0, f"모든 잔고({initial_balance})가 투자되어 0이 되어야 합니다"

    def test_save_and_get_strategy(self, strategy_repo: FakeStrategyRepository, strategy_create_command: StrategyCreateCommand):
        """전략을 저장하고 조회하는 테스트"""
        # Given
        saved_strategy = strategy_repo.save(strategy_create_command)

        # When
        found_strategy = strategy_repo.find_by_id(saved_strategy.id)
        found_strategies = strategy_repo.find_all()

        # Then
        assert found_strategy == saved_strategy, "저장된 전략과 조회된 전략이 동일해야 합니다"
        assert len(found_strategies) == 1, "전체 조회 시 전략이 1개 있어야 한다"
        assert found_strategies[0] == saved_strategy, "전체 조회 시 저장된 전략이 포함되어야 한다"

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
