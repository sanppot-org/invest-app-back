from fastapi import FastAPI
import domain.chat_client as chat
import domain.kis_api_helper_kr as kis_kr
import domain.env.env as env

app = FastAPI()


@app.get("/")
def root():
    return f"ENV: {env.get_env_type()} Prop: {env.get_prop()}"


@app.put("/change-env")
def change_env():
    env.change_env()
    return env.get_env_type()


@app.get("/balance")
def get_account():
    return kis_kr.get_balance()
