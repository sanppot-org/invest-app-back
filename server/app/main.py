import schedule
import uvicorn
from fastapi import FastAPI
import domain.chat_client as chat
from domain.helper import KIS_Common as common
from domain.helper import KIS_API_Helper_KR as kis_kr
from infra import strategy_repo
from infra.schema import Strategy
from web.strategy_req import StrategyReq


app = FastAPI()


@app.get("/")
def root():
    return f"ENV: {common.GetNowDist()} Prop: {common.stock_info}"


@app.put("/change-env")
def change_env():
    if common.GetNowDist() == "REAL":
        common.SetChangeMode("VIRTUAL")
    else:
        common.SetChangeMode("REAL")
    return common.GetNowDist()


@app.get("/balance")
def get_account():
    return kis_kr.GetBalance()


@app.get("/strategies")
def find_all_strategy():
    return strategy_repo.find_all()


@app.post("/strategies")
def create_strategy(req: StrategyReq):
    return strategy_repo.save(Strategy(name=req.name))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
