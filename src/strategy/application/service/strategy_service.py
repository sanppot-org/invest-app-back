from datetime import datetime
from typing import Dict
from src.common.adapter.out import slack_noti_client
from src.common.application.port.out.time_holder import TimeHolder
from src.common.application.port.out.stock_market_port import StockMarketQueryPort
from src.account.application.service.account_provider import AccountProvider
from src.account.domain.account import Account
from src.account.domain.holdings import HoldingsInfo
from src.common.application.port.out.repository import *
from src.common.domain.ticker import Ticker
from src.strategy.application.port.out.strategy_repository import StrategyRepository
from src.strategy.domain.stock_info import StockInfo
from src.strategy.domain.strategy import Strategy
from dependency_injector.wiring import inject
from src.common.domain.logging_config import logger


class StrategyService:
    @inject
    def __init__(
        self,
        strategy_repo: StrategyRepository,
        account_provider: AccountProvider,
        stock_market_query_port: StockMarketQueryPort,
        time_holder: TimeHolder,
    ):
        self.strategy_repo = strategy_repo
        self.account_provider = account_provider
        self.stock_market_query_port = stock_market_query_port
        self.time_holder = time_holder

    def rebalance(self, strategy: Strategy, is_force: bool = False):
        if not is_force:
            now: datetime = self.time_holder.get_now()

            # 리밸런싱 조건 확인
            strategy.check_is_time_to_rebalance(now)

        # 주식 시장 열려있는지 확인
        self.stock_market_query_port.is_market_open(strategy.get_market())

        account: Account = self.account_provider.get_account(strategy.get_account_id())

        # 2. 포트폴리오 할당 금액 계산 (포트 폴리오 비중 * 잔고)
        invest_amount: float = strategy.get_invest_amount(account.get_balance())
        logger.info(f"invest_amount: {invest_amount}")

        # 3. 보유 종목 리스트 조회
        holddings_dict: Dict[str, HoldingsInfo] = account.get_holdings()

        stocks: Dict[str, StockInfo] = strategy.get_stocks()

        # 4. 종목별 비중 계산
        for ticker, stock in stocks.items():
            ticker = Ticker(ticker)
            current_price = self.stock_market_query_port.get_current_price(ticker)
            stock.calculate_rebalance_amt(
                portfolio_target_amt=invest_amount,
                holdings=holddings_dict.get(ticker.get_kr_ticker()),
                current_price=current_price,
            )

        # 5. 리밸런싱 수량 만큼 매도
        for ticker, stock in stocks.items():
            if stock.rebalance_qty < 0:
                account.sell_market_order(Ticker(ticker), stock.rebalance_qty)

        # 6. 리밸런싱 수량 만큼 매수
        for ticker, stock in stocks.items():
            if stock.rebalance_qty > 0:
                account.buy_market_order(Ticker(ticker), stock.rebalance_qty)

        strategy.complete()

        self.strategy_repo.save(strategy)

    def rebalance_all(self):
        strategies = self.strategy_repo.find_all_active()
        for strategy in strategies:
            self.rebalance(strategy)

    def trade(self, strategy_id: int):
        try:
            strategy = self.strategy_repo.find_by_id(strategy_id)
            account = self.account_provider.get_account(strategy.account_id)
            strategy.trade(account)
            self.strategy_repo.update(strategy_id, strategy)
        except Exception as e:
            slack_noti_client.send_exception(f"전략 실행 오류: {e}")
            raise e
