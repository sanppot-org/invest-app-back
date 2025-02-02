import json
from typing import Dict, override

import requests
from src.account.domain.account import Account
from src.account.domain.account_info import AccountInfo
from src.account.domain.holdings import HoldingsInfo
from src.common.adapter.out.stock_market_client import StockMarketClient
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.domain.type import BrokerType, Market, OrderType
from src.account.domain.access_token import AccessToken
from src.account.adapter.out.kis.dto import BalanceResponse
from src.common.domain.ticker import Ticker
from src.common.domain.logging_config import logger

stock_market_client = StockMarketClient()


class KisAccount(Account):
    def __init__(self, account_info: AccountInfo, is_virtual: bool = False):
        super().__init__(account_info=account_info)

        if account_info.broker_type != BrokerType.KIS:
            raise InvestAppException(ExeptionType.INVALID_ACCOUNT_TYPE, account_info.broker_type)

        self.is_virtual: bool = is_virtual
        self.access_token: AccessToken | None = self.account_info.token

    @override
    def get_balance(self, market: Market = Market.KR) -> float:
        if market.is_kr():
            return BalanceResponse.of(self._get_balance_kr()["output2"][0]).total_money

        # TODO: 제대로 구현하기
        return self._get_balance_us()

    @override
    def sell_all(self, ticker: str) -> None:
        raise NotImplementedError

    @override
    def buy_limit_order(self, ticker: Ticker, price: float, quantity: float):
        raise NotImplementedError

    @override
    def sell_market_order(self, ticker: Ticker, quantity: float) -> None:
        logger.info(f"sell_market_order: {ticker}, {quantity}")
        if ticker.is_kr():
            self._make_order_kr(ticker.get_kr_ticker(), quantity, OrderType.SELL)
            return

        target_price = self._get_current_price(ticker.value) * 1.1
        return self._make_order_us(ticker.value, quantity, target_price, OrderType.SELL)

    @override
    def buy_market_order(self, ticker: Ticker, quantity: float) -> None:
        logger.info(f"buy_market_order: {ticker}, {quantity}")
        if ticker.is_kr():
            self._make_order_kr(ticker.get_kr_ticker(), quantity, OrderType.BUY)
            return

        target_price = self._get_current_price(ticker.value) * 1.1
        self._make_order_us(ticker.value, quantity, target_price, OrderType.BUY)

    @override
    def get_holdings(self, market: Market = Market.KR) -> Dict[str, HoldingsInfo]:
        if market.is_kr():
            return {
                stock["pdno"]: HoldingsInfo(
                    name=stock["prdt_name"],
                    quantity=float(stock["hldg_qty"]),
                    avg_price=float(stock["pchs_avg_pric"]),
                    eval_amt=float(stock["evlu_amt"]),
                )
                for stock in self._get_balance_kr()["output1"]
            }

        return {
            stock["ovrs_pdno"]: HoldingsInfo(
                name=stock["ovrs_item_name"],
                quantity=float(stock["ovrs_cblc_qty"]),
                avg_price=float(stock["pchs_avg_pric"]),
                eval_amt=float(stock["ovrs_stck_evlu_amt"]),
            )
            for stock in self._get_balance_us()["output1"]
        }

    def refresh_token(self):
        if self.is_token_invalid():
            self.account_info.token = self._generate_token()
            logger.info(f"토큰 갱신 완료. account_id={self.account_info.id}")

    def is_token_invalid(self) -> bool:
        return self.access_token is None or self.access_token.is_expired()

    @override
    def get_total_principal(self) -> float:
        raise NotImplementedError

    @override
    def get_revenue(self) -> float:
        raise NotImplementedError

    @override
    def sell_all_holdings(self) -> None:
        raise NotImplementedError

    def _get_current_price(self, ticker: str) -> float:
        return stock_market_client.get_current_price(ticker)

    def _get_balance_kr(self) -> dict:
        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token.token}",
            "appKey": self.account_info.app_key,
            "appSecret": self.account_info.secret_key,
            "tr_id": "VTTC8434R" if self.is_virtual else "TTTC8434R",
            "custtype": "P",
        }

        params = {
            "CANO": self.account_info.number,
            "ACNT_PRDT_CD": self.account_info.product_code,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
        }

        URL = f"{self.account_info.url_base}/uapi/domestic-stock/v1/trading/inquire-balance"

        res = requests.get(URL, headers=headers, params=params)

        if res.status_code == 200 and res.json()["rt_cd"] == "0":
            return res.json()

        raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, res.text)

    def _get_balance_us(self) -> dict:
        URL = f"{self.account_info.url_base}/uapi/overseas-stock/v1/trading/inquire-present-balance"

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {self.access_token.token}",
            "appKey": self.account_info.app_key,
            "appSecret": self.account_info.secret_key,
            "tr_id": "VTRP6504R" if self.is_virtual else "CTRP6504R",
            "custtype": "P",
        }

        params = {
            "CANO": self.account_info.number,
            "ACNT_PRDT_CD": self.account_info.product_code,
            "WCRC_FRCR_DVSN_CD": "02",
            "NATN_CD": "840",
            "TR_MKET_CD": "00",
            "INQR_DVSN_CD": "00",
        }

        res = requests.get(URL, headers=headers, params=params)

        if res.status_code == 200 and res.json()["rt_cd"] == "0":
            return res.json()

            # # 실시간 주식 상태가 반영이 안되서 주식 정보를 직접 읽어서 계산!
            # my_stock_list = GetMyStockList(st)

            # StockOriMoneyTotal = 0
            # StockNowMoneyTotal = 0

            # for stock in my_stock_list:
            #     # pprint.pprint(stock)
            #     StockOriMoneyTotal += float(stock["StockOriMoney"])
            #     StockNowMoneyTotal += float(stock["StockNowMoney"])

            #     # print("--", StockNowMoneyTotal, StockOriMoneyTotal)

            # balanceDict = dict()
            # balanceDict["RemainMoney"] = 0

            # Rate = 1200

            # if st == "USD":

            #     for data in result:
            #         if data["crcy_cd"] == "USD":
            #             # 예수금 총금액 (즉 주문가능 금액)
            #             balanceDict["RemainMoney"] = (
            #                 float(data["frcr_dncl_amt_2"])
            #                 - float(data["frcr_buy_amt_smtl"])
            #                 + float(data["frcr_sll_amt_smtl"])
            #             )  # 모의계좌는 0으로 나온다 이유는 모르겠음!
            #             Rate = data["frst_bltn_exrt"]
            #             break

            #     result = res.json()["output3"]

            #     # 임시로 모의 계좌 잔고가 0으로
            #     if (
            #         common.GetNowDist() == "VIRTUAL"
            #         and float(balanceDict["RemainMoney"]) == 0
            #     ):

            #         # 주식 총 평가 금액
            #         balanceDict["stock_money"] = (
            #             StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
            #         )
            #         # 평가 손익 금액
            #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
            #             StockOriMoneyTotal
            #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

            #         balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"]) / float(
            #             Rate
            #         )

            #         # 총 평가 금액
            #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
            #             balanceDict["RemainMoney"]
            #         )

            #     else:

            #         # 주식 총 평가 금액
            #         balanceDict["stock_money"] = (
            #             StockNowMoneyTotal  # (float(result['evlu_amt_smtl_amt']) / float(Rate))
            #         )
            #         # 평가 손익 금액
            #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
            #             StockOriMoneyTotal
            #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

            #         # 총 평가 금액
            #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
            #             balanceDict["RemainMoney"]
            #         )

            # else:

            #     for data in result:
            #         if data["crcy_cd"] == "USD":
            #             Rate = data["frst_bltn_exrt"]
            #             # 예수금 총금액 (즉 주문가능현금)
            #             balanceDict["RemainMoney"] = (
            #                 float(data["frcr_dncl_amt_2"])
            #                 - float(data["frcr_buy_amt_smtl"])
            #                 + float(data["frcr_sll_amt_smtl"])
            #             ) * float(Rate)
            #             # balanceDict['RemainMoney'] = data['frcr_evlu_amt2'] #모의계좌는 0으로 나온다 이유는 모르겠음!

            #             break

            #     # print("balanceDict['RemainMoney'] ", balanceDict['RemainMoney'] )

            #     result = res.json()["output3"]

            #     # 임시로 모의 계좌 잔고가 0으로 나오면
            #     if (
            #         common.GetNowDist() == "VIRTUAL"
            #         and float(balanceDict["RemainMoney"]) == 0
            #     ):

            #         # 주식 총 평가 금액
            #         balanceDict["stock_money"] = (
            #             StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
            #         )
            #         # 평가 손익 금액
            #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
            #             StockOriMoneyTotal
            #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

            #         balanceDict["RemainMoney"] = float(result["frcr_evlu_tota"])

            #         # 총 평가 금액
            #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
            #             balanceDict["RemainMoney"]
            #         )

            #     else:

            #         # 주식 총 평가 금액
            #         balanceDict["stock_money"] = (
            #             StockNowMoneyTotal  # result['evlu_amt_smtl_amt']
            #         )
            #         # 평가 손익 금액
            #         balanceDict["StockRevenue"] = float(StockNowMoneyTotal) - float(
            #             StockOriMoneyTotal
            #         )  # round((float(StockNowMoneyTotal)/float(StockOriMoneyTotal) - 1.0) * 100.0,2)

            #         # 총 평가 금액
            #         balanceDict["total_money"] = float(balanceDict["stock_money"]) + float(
            #             balanceDict["RemainMoney"]
            #         )

            # return balanceDict

        raise InvestAppException(ExeptionType.FAILED_TO_GET_BALANCE, res.text)

    def _generate_token(self) -> AccessToken | None:
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.account_info.app_key,
            "appsecret": self.account_info.secret_key,
        }
        URL = f"{self.account_info.url_base}/oauth2/tokenP"

        try:
            res = requests.post(URL, headers=headers, data=json.dumps(body))
        except Exception as e:
            logger.error(f"Failed to create token: {e}")
            return None

        if res.status_code != 200:
            raise InvestAppException(ExeptionType.FAILED_TO_CREATE_TOKEN, res.text)

        res_body = res.json()
        return AccessToken(token=res_body["access_token"], expiration=res_body["access_token_token_expired"])

    def _make_order_kr(self, ticker: str, quantity: float, order_type: OrderType) -> None:
        tr_id = "VTTC0801U" if self.is_virtual else "TTTC0801U"

        if order_type.is_buy():
            tr_id = "VTTC0802U" if self.is_virtual else "TTTC0802U"

        PATH = "uapi/domestic-stock/v1/trading/order-cash"
        URL = f"{self.account_info.url_base}/{PATH}"
        headers = {
            "authorization": f"Bearer {self.access_token.token}",
            "appKey": self.account_info.app_key,
            "appSecret": self.account_info.secret_key,
            "tr_id": tr_id,
        }
        data = {
            "CANO": self.account_info.number,
            "ACNT_PRDT_CD": self.account_info.product_code,
            "PDNO": ticker,
            "ORD_DVSN": "01",  # 시장가
            "ORD_QTY": str(abs(quantity)),
            "ORD_UNPR": "0",
        }
        res = requests.post(URL, headers=headers, data=json.dumps(data))

        if res.status_code == 200 and res.json()["rt_cd"] == "0":
            return res.json()

        raise InvestAppException(ExeptionType.FAILED_TO_ORDER, res.text)

    def _make_order_us(self, ticker: str, quantity: float, price: float, order_type: OrderType) -> None:
        tr_id = "VTTT1001U" if self.is_virtual else "TTTT1006U"

        if order_type.is_buy():
            tr_id = "VTTT1002U" if self.is_virtual else "TTTT1002U"

        PATH = "uapi/overseas-stock/v1/trading/order"
        URL = f"{self.account_info.url_base}/{PATH}"
        headers = {
            "authorization": f"Bearer {self.access_token.token}",
            "appKey": self.account_info.app_key,
            "appSecret": self.account_info.secret_key,
            "tr_id": tr_id,
        }
        data = {
            "CANO": self.account_info.number,
            "ACNT_PRDT_CD": self.account_info.product_code,
            "OVRS_EXCG_CD": "NASD",  # TODO : 거래소 코드 고도화
            "PDNO": ticker,
            "ORD_QTY": str(quantity),
            "OVRS_ORD_UNPR": str(price),
            "ORD_SVR_DVSN_CD": "0",
            "ORD_DVSN": "00",
        }

        res = requests.post(URL, headers=headers, data=json.dumps(data))

        if res.status_code == 200 and res.json()["rt_cd"] == "0":
            return res.json()

        raise InvestAppException(ExeptionType.FAILED_TO_ORDER, res.text)


class KisRealAccount(KisAccount):
    def __init__(self, account_info: AccountInfo):
        super().__init__(account_info=account_info)


class KisVirtualAccount(KisAccount):
    def __init__(self, account_info: AccountInfo):
        super().__init__(account_info=account_info, is_virtual=True)
