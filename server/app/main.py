from fastapi import FastAPI
import domain.kis_common as common

app = FastAPI()


@app.get("/")
def read_root():
    return common.get_app_key()
