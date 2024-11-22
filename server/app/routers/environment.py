from fastapi import APIRouter
from domain.helper import KIS_Common as common

router = APIRouter(prefix="/env", tags=["environment"])


@router.get("/")
def get_env():
    return f"ENV: {common.GetNowDist()} Prop: {common.stock_info}"


@router.put("/change")
def change_env():
    if common.GetNowDist() == "REAL":
        common.SetChangeMode("VIRTUAL")
    else:
        common.SetChangeMode("REAL")
    return common.GetNowDist()
