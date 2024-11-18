from domain import kis_util
from domain.stock_info import StockInfo, StockList
from domain.type import EnvType


class StaticAsset:
    def __init__(
        self, portfolio_name: str, invest_rate: float, portfolio_stock_list: StockList
    ):
        self.__env: EnvType = EnvType.REAL
        self.portfolio_name: str = portfolio_name
        self.invest_rate: float = invest_rate
        self.portfolio_stock_list: StockList = portfolio_stock_list

    def trade(self):
        # 1. 장이 열렸는지 확인
        if not kis_util.is_market_open():
            return

        # TODO : 2. 리밸런스 했는지 확인

        # 3. 잔고 조회
        balance = kis_util.get_balance()

        total_money = float(balance["total_money"]) * self.invest_rate

        my_stock_list = kis_util.get_my_stock_list()

        stock_info: StockInfo
        for stock_info in self.portfolio_stock_list:
            stock_info.code
