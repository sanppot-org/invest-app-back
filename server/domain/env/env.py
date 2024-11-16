import yaml
from abc import ABC, abstractmethod
from domain.env.env_type import EnvType

stock_info = None

with open("config/hantu-stock-config.yml", encoding="UTF-8") as f:
    stock_info = yaml.load(f, Loader=yaml.FullLoader)

real_stock_info = stock_info["real"]
virtual_stock_info = stock_info["virtual"]


class Env(ABC):
    @abstractmethod
    def is_real(self) -> bool:
        pass

    @abstractmethod
    def get_env_type(self) -> EnvType:
        pass

    @abstractmethod
    def get_prop(self) -> dict:
        pass

    @abstractmethod
    def get_tr_id_get_balance(self) -> str:
        pass


class RealEnv(Env):
    def is_real(self) -> bool:
        return True

    def get_env_type(self) -> EnvType:
        return EnvType.REAL

    def get_prop(self) -> dict:
        return real_stock_info

    def get_tr_id_get_balance(self) -> str:
        return "TTTC8434R"


class VirtualEnv(Env):
    def is_real(self) -> bool:
        return False

    def get_env_type(self) -> EnvType:
        return EnvType.VIRTUAL

    def get_prop(self) -> dict:
        return virtual_stock_info

    def get_tr_id_get_balance(self) -> str:
        return "VTTC8434R"


real_env: Env = RealEnv()
virtual_env: Env = VirtualEnv()
env: Env = real_env


def get_env_type() -> EnvType:
    return env.get_env_type()


def change_env():
    global env
    env = virtual_env if env.is_real() else real_env


def get_prop() -> dict:
    return env.get_prop()


def get_app_key() -> str:
    return env.get_prop()["app-key"]


def get_app_secret() -> str:
    return env.get_prop()["app-secret"]


def get_tr_id_get_balance() -> str:
    return env.get_tr_id_get_balance()


def get_account_no() -> str:
    return env.get_prop()["cano"]


def get_account_prd_no() -> str:
    return env.get_prop()["acnt-prdt-cd"]


def get_url_base() -> str:
    return env.get_prop()["url-base"]


def get_token_path() -> str:
    return env.get_prop()["token-path"]
