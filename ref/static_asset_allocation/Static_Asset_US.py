# -*- coding: utf-8 -*-
"""
하다가 잘 안되시면 계속 내용이 추가되고 있는 아래 FAQ를 꼭꼭 체크하시고

주식/코인 자동매매 FAQ
https://blog.naver.com/zacra/223203988739

그래도 안 된다면 구글링 해보시고
그래도 모르겠다면 클래스 댓글, 블로그 댓글, 단톡방( https://blog.naver.com/zacra/223111402375 )에 질문주세요! ^^

클래스 제작 완료 후 많은 시간이 흘렀고 그 사이 전략에 많은 발전이 있었습니다.
제가 직접 투자하고자 백테스팅으로 검증하여 더 안심하고 있는 자동매매 전략들을 블로그에 공개하고 있으니
완강 후 꼭 블로그&유튜브 심화 과정에 참여해 보세요! 기다릴께요!!

아래 빠른 자동매매 가이드 시간날 때 완독하시면 방향이 잡히실 거예요!
https://blog.naver.com/zacra/223086628069

  
"""
from domain.helper import KIS_Common as common
from src.infra import chat_client
import time
import json
import pprint

from src.domain.static_asset_allocation import kis_util


# 1. 포트폴리오 이름
portfolio_name = "정적자산배분전략_영구변형"


# 2. 계좌 선택.. "VIRTUAL" 는 모의 계좌!
common.SetChangeMode("VIRTUAL")  # REAL or VIRTUAL


#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

# 전제는 크롭탭에 주말 빼고 UTC 0시 기준 16시/ 우리나라 시간 새벽1시 정각에 해당 봇이 돈다고 가정!
# 0 16 * * 1-5 python3 /var/autobot/Static_Asset_US.py

BOT_NAME = f"{common.GetNowDist()}_MyStaticAssetBotUS"

# 파일 경로입니다.
static_asset_tym_file_path = f"/var/autobot/{BOT_NAME}_YM1.json"


def get_YM_dict() -> dict:
    try:
        # 파일에 저장된 년월 문자열 (ex> 2022_9)를 읽는다
        with open(static_asset_tym_file_path, "r") as json_file:
            return json.load(json_file)

    except Exception as e:
        print("Exception by First")

    return YMDict


YMDict = get_YM_dict()

# 시간 정보를 읽는다
time_info = time.gmtime()
# 년월 문자열을 만든다 즉 2022년 9월이라면 2022_9 라는 문자열이 만들어져 strYM에 들어간다!
strYM = f"{time_info.tm_year}_{time_info.tm_mon}"
print("ym_st: ", strYM)


# 리밸런싱이 가능한지 여부를 판단!
is_rebalance_go: bool = False

# 만약 키가 존재 하지 않는다 즉 아직 한번도 매매가 안된 상태라면 or 이번 달에 리밸런스하지 않은 경우
if YMDict.get("ym_st") == None or YMDict["ym_st"] != strYM:
    # 리밸런싱 가능! (리밸런싱이라기보다 첫 매수해야 되는 상황!)
    is_rebalance_go = True


# 강제 리밸런싱 수행!
# is_rebalance_go = True


# 마켓이 열렸는지 여부~!
is_market_open = kis_util.is_market_open()

if is_market_open == True and is_rebalance_go:
    print("Market Is Open!!!!!!!!!!!")
    # 영상엔 없지만 리밸런싱이 가능할때만 내게 메시지를 보내자!
    chat_client.send_message(f"{portfolio_name} ({strYM}) 장이 열려서 포트폴리오 리밸런싱 가능!!")

else:
    print("Market Is Close!!!!!!!!!!!")
    # 영상엔 없지만 리밸런싱이 가능할때만 내게 메시지를 보내자!
    if is_rebalance_go == True:
        chat_client.send_message(f"{portfolio_name} ({strYM}) 장이 닫혀서 포트폴리오 리밸런싱 불가능!!")


#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################


# 계좌 잔고를 가지고 온다!
balance = kis_util.get_balance()

print("--------------내 보유 잔고---------------------")
pprint.pprint(balance)
print("--------------------------------------------")
# 총 평가금액에서 해당 봇에게 할당할 총 금액비율 1.0 = 100%  0.5 = 50%
invest_rate = 0.04

# 기준이 되는 내 총 평가금액에서 투자비중을 곱해서 나온 포트폴리오에 할당된 돈!!
total_money = float(balance["total_money"]) * invest_rate

print("총 포트폴리오에 할당된 투자 가능 금액 : $", total_money)

"""
영구 포트폴리오 변형

(주식) 25% stock
SPY             10%  - S&P 500
QQQ             10%  - 나스닥 추종
EEM              5%  - 이머징 마켓 주식 우리나라 주식도 포함이 되어 있어요~

(채권) 25% bond
TLT             12.5% - 미국 장기채
LTPZ            12.5% -물가 연동채

(금) 25% gold
GLD          12.5% - 금
DBC          12.5% - 원자재

(현금) 25% cash
BIL      12.5% - 초 단기 채권
SHY       12.5% - 단기 채권

"""

##########################################################

# 투자 주식 리스트 설정
my_portfolio_list = list()


stock1 = dict()
stock1["stock_code"] = "SPY"  # 종목코드
stock1["stock_target_rate"] = 10.0  # 포트폴리오 목표 비중
stock1["stock_rebalance_amt"] = 0  # 리밸런싱 해야하는 수량


my_portfolio_list.append(stock1)

stock2 = dict()
stock2["stock_code"] = "QQQ"
stock2["stock_target_rate"] = 10.0
stock2["stock_rebalance_amt"] = 0


my_portfolio_list.append(stock2)

stock3 = dict()
stock3["stock_code"] = "EEM"
stock3["stock_target_rate"] = 5.0
stock3["stock_rebalance_amt"] = 0


my_portfolio_list.append(stock3)


bond1 = dict()
bond1["stock_code"] = "TLT"
bond1["stock_target_rate"] = 12.5
bond1["stock_rebalance_amt"] = 0

my_portfolio_list.append(bond1)

bond2 = dict()
bond2["stock_code"] = "LTPZ"
bond2["stock_target_rate"] = 12.5
bond2["stock_rebalance_amt"] = 0


my_portfolio_list.append(bond2)


gold1 = dict()
gold1["stock_code"] = "GLD"
gold1["stock_target_rate"] = 12.5
gold1["stock_rebalance_amt"] = 0


my_portfolio_list.append(gold1)

gold2 = dict()
gold2["stock_code"] = "DBC"
gold2["stock_target_rate"] = 12.5
gold2["stock_rebalance_amt"] = 0

my_portfolio_list.append(gold2)


cash1 = dict()
cash1["stock_code"] = "BIL"
cash1["stock_target_rate"] = 12.5
cash1["stock_rebalance_amt"] = 0


my_portfolio_list.append(cash1)


cash2 = dict()
cash2["stock_code"] = "SHY"
cash2["stock_target_rate"] = 12.5
cash2["stock_rebalance_amt"] = 0


my_portfolio_list.append(cash2)

"""
#금액 대비 적합한 포트폴리오인지 체크
for stock_info in my_portfolio_list:

    #내주식 코드
    stock_code = stock_info['stock_code']
    stock_target_rate = float(stock_info['stock_target_rate']) / 100.0

    #현재가!
    current_price = kis_util.get_current_price(stock_code)


    #비중대로 매수할 총 금액을 계산한다 
    stock_money = total_money * stock_target_rate

    #매수할 수량을 계산한다!
    Amt = int(stock_money / current_price)

    print("stock_code " , stock_code , " buy_amt", Amt)
"""


##########################################################

print("--------------내 보유 주식---------------------")
# 그리고 현재 이 계좌에서 보유한 주식 리스트를 가지고 옵니다!
my_stock_list = kis_util.get_my_stock_list()
pprint.pprint(my_stock_list)
print("--------------------------------------------")
##########################################################


print("--------------리밸런싱 수량 계산 ---------------------")

str_result = "-- 현재 포트폴리오 상황 --\n"

# 매수된 자산의 총합!
total_stock_money = 0

# 현재 평가금액 기준으로 각 자산이 몇 주씩 매수해야 되는지 계산한다 (포트폴리오 비중에 따라) 이게 바로 리밸런싱 목표치가 됩니다.
for stock_info in my_portfolio_list:

    # 내주식 코드
    stock_code = stock_info["stock_code"]
    stock_target_rate = float(stock_info["stock_target_rate"]) / 100.0

    # 현재가!
    current_price = kis_util.get_current_price(stock_code)

    stock_name = ""
    stock_amt = 0  # 수량
    stock_avg_price = 0  # 평단
    stock_eval_totalmoney = 0  # 총평가금액!
    stock_revenue_rate = 0  # 종목 수익률
    stock_revenue_money = 0  # 종목 수익금

    # 내가 보유한 주식 리스트에서 매수된 잔고 정보를 가져온다
    for my_stock in my_stock_list:
        if my_stock["StockCode"] == stock_code:
            stock_name = my_stock["StockName"]
            stock_amt = int(my_stock["StockAmt"])
            stock_avg_price = float(my_stock["StockAvgPrice"])
            stock_eval_totalmoney = float(my_stock["StockNowMoney"])
            stock_revenue_rate = float(my_stock["StockRevenueRate"])
            stock_revenue_money = float(my_stock["StockRevenueMoney"])

            break

    print("##### stock_code: ", stock_code)
    print("---> TargetRate:", round(stock_target_rate * 100.0, 2), "%")

    # 주식의 총 평가금액을 더해준다
    total_stock_money += stock_eval_totalmoney

    # 현재 비중
    stock_now_rate = 0

    # 잔고에 있는 경우 즉 이미 매수된 주식의 경우
    if stock_amt > 0:

        stock_now_rate = round((stock_eval_totalmoney / total_money), 3)

        print("---> NowRate:", round(stock_now_rate * 100.0, 2), "%")

        # 목표한 비중가 다르다면!!
        if stock_now_rate != stock_target_rate:

            # 갭을 구한다!!!
            gap_rate = stock_target_rate - stock_now_rate

            # 그래서 그 갭만큼의 금액을 구한다
            gap_money = total_money * abs(gap_rate)
            # 현재가로 나눠서 몇주를 매매해야 되는지 계산한다
            gap_amt = gap_money / current_price

            # 수량이 1보다 커야 리밸러싱을 할 수 있다!! 즉 그 전에는 리밸런싱 불가
            if gap_amt >= 1.0:

                gap_amt = int(gap_amt)

                # 갭이 음수라면! 비중이 더 많으니 팔아야 되는 상황!!!
                if gap_rate < 0:

                    # 팔아야 되는 상황에서는 현재 주식수량에서 매도할 수량을 뺀 값이 1주는 남아 있어야 한다
                    # 그래야 포트폴리오 상에서 아예 사라지는 걸 막는다!
                    if stock_amt - gap_amt >= 1:
                        stock_info["stock_rebalance_amt"] = -gap_amt

                # 갭이 양수라면 비중이 더 적으니 사야되는 상황!
                else:
                    stock_info["stock_rebalance_amt"] = gap_amt

    # 잔고에 없는 경우
    else:

        print("---> NowRate: 0%")

        # 잔고가 없다면 첫 매수다! 비중대로 매수할 총 금액을 계산한다
        buy_money = total_money * stock_target_rate

        # 매수할 수량을 계산한다!
        buy_amt = int(buy_money / current_price)

        # 포트폴리오에 들어간건 일단 무조건 1주를 사주자... 아니라면 아래 2줄 주석처리
        # if buy_amt <= 0:
        #    buy_amt = 1

        stock_info["stock_rebalance_amt"] = buy_amt

    # 라인 메시지랑 로그를 만들기 위한 문자열
    line_data = (
        ">> "
        + stock_code
        + " << \n비중: "
        + str(round(stock_now_rate * 100.0, 2))
        + "/"
        + str(round(stock_target_rate * 100.0, 2))
        + "% \n수익: $"
        + str(stock_revenue_money)
        + "("
        + str(round(stock_revenue_rate, 2))
        + "%) \n총평가금액: $"
        + str(round(stock_eval_totalmoney, 2))
        + "\n리밸런싱수량: "
        + str(stock_info["stock_rebalance_amt"])
        + "\n----------------------\n"
    )

    # 만약 아래 한번에 보내는 라인메시지가 짤린다면 아래 주석을 해제하여 개별로 보내면 됩니다
    # if is_rebalance_go == True:
    #    chat_client.send_message(line_data)
    str_result += line_data


##########################################################

print("--------------리밸런싱 해야 되는 수량-------------")

data_str = (
    "\n"
    + portfolio_name
    + "\n"
    + str_result
    + "\n포트폴리오할당금액: $"
    + str(round(total_money, 2))
    + "\n매수한자산총액: $"
    + str(round(total_stock_money, 2))
)

# 결과를 출력해 줍니다!
print(data_str)

# 영상엔 없지만 리밸런싱이 가능할때만 내게 메시지를 보내자!
if is_rebalance_go == True:
    chat_client.send_message(data_str)

# 만약 위의 한번에 보내는 라인메시지가 짤린다면 아래 주석을 해제하여 개별로 보내면 됩니다
# if is_rebalance_go == True:
#    chat_client.send_message("\n포트폴리오할당금액: $" + str(round(total_money,2)) + "\n매수한자산총액: $" + str(round(total_stock_money,2)))


print("--------------------------------------------")

##########################################################


# 리밸런싱이 가능한 상태여야 하고 매수 매도는 장이 열려있어야지만 가능하다!!!
if is_rebalance_go == True and is_market_open == True:

    chat_client.send_message(portfolio_name + " (" + strYM + ") 리밸런싱 시작!!")

    print("------------------리밸런싱 시작  ---------------------")
    # 이제 목표치에 맞게 포트폴리오를 조정하면 되는데
    # 매도를 해야 돈이 생겨 매수를 할 수 있을 테니
    # 먼저 매도를 하고
    # 그 다음에 매수를 해서 포트폴리오를 조정합니다!

    print("--------------매도 (리밸런싱 수량이 마이너스인거)---------------------")

    for stock_info in my_portfolio_list:

        # 내주식 코드
        stock_code = stock_info["stock_code"]
        rebalance_amt = stock_info["stock_rebalance_amt"]

        # 리밸런싱 수량이 마이너스인 것을 찾아 매도 한다!
        if rebalance_amt < 0:

            # 현재가!
            current_price = kis_util.get_current_price(stock_code)

            # 현재가보다 아래에 매도 주문을 넣음으로써 시장가로 매도
            current_price *= 0.9
            pprint.pprint(kis_util.make_sell_limit_order(stock_code, abs(rebalance_amt), current_price))

    print("--------------------------------------------")

    # 3초 정도 쉬어준다
    time.sleep(3.0)

    print("--------------매수 ---------------------")

    for stock_info in my_portfolio_list:

        # 내주식 코드
        stock_code = stock_info["stock_code"]
        rebalance_amt = stock_info["stock_rebalance_amt"]

        # 리밸런싱 수량이 플러스인 것을 찾아 매수 한다!
        if rebalance_amt > 0:

            # 현재가!
            current_price = kis_util.get_current_price(stock_code)

            # 현재가보다 위에 매수 주문을 넣음으로써 시장가로 매수
            current_price *= 1.1
            pprint.pprint(kis_util.make_buy_limit_order(stock_code, rebalance_amt, current_price))

    print("--------------------------------------------")

    #########################################################################################################################
    # 첫 매수던 리밸런싱이던 매매가 끝났으면 이달의 리밸런싱은 끝이다. 해당 달의 년달 즉 22년 9월이라면 '2022_9' 라는 값을 파일에 저장해 둔다!
    # 파일에 저장하는 부분은 여기가 유일!!!!
    YMDict["ym_st"] = strYM
    with open(static_asset_tym_file_path, "w") as outfile:
        json.dump(YMDict, outfile)
    #########################################################################################################################

    chat_client.send_message(portfolio_name + " (" + strYM + ") 리밸런싱 완료!!")
    print("------------------리밸런싱 끝---------------------")
