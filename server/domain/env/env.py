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

    @abstractmethod
    def get_tr_id_buy(self) -> str:
        pass

    @abstractmethod
    def get_tr_id_sell(self) -> str:
        pass

    @abstractmethod
    def get_tr_id_psbl_order(self) -> str:
        pass

    @abstractmethod
    def get_tr_id_order_list(self) -> str:
        pass

    @abstractmethod
    def get_tr_id_cancel_order(self) -> str:
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

    def get_tr_id_buy(self) -> str:
        return "TTTC0802U"

    def get_tr_id_sell(self) -> str:
        return "TTTC0801U"

    def get_tr_id_psbl_order(self) -> str:
        return "TTTC8908R"

    def get_tr_id_order_list(self) -> str:
        return "TTTC8001R"

    def get_tr_id_cancel_order(self) -> str:
        return "TTTC0803U"


class VirtualEnv(Env):
    def is_real(self) -> bool:
        return False

    def get_env_type(self) -> EnvType:
        return EnvType.VIRTUAL

    def get_prop(self) -> dict:
        return virtual_stock_info

    def get_tr_id_get_balance(self) -> str:
        return "VTTC8434R"

    def get_tr_id_buy(self) -> str:
        return "VTTC0802U"

    def get_tr_id_sell(self) -> str:
        return "VTTC0801U"

    def get_tr_id_psbl_order(self) -> str:
        return "VTTC8908R"

    def get_tr_id_order_list(self) -> str:
        return "VTTC8001R"

    def get_tr_id_cancel_order(self) -> str:
        return "VTTC0803U"


real_env: Env = RealEnv()
virtual_env: Env = VirtualEnv()
env: Env = real_env


def is_real() -> bool:
    return env.is_real()


def get_env_type() -> EnvType:
    return env.get_env_type()


def change_env():
    global env
    env = virtual_env if env.is_real() else real_env


def set_env(env_type: EnvType):
    global env
    env = real_env if env_type == EnvType.REAL else virtual_env


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


def get_tr_id_buy() -> str:
    return env.get_tr_id_buy()


def get_tr_id_sell() -> str:
    return env.get_tr_id_sell()


def get_tr_id_psbl_order() -> str:
    return env.get_tr_id_psbl_order()


def get_tr_id_order_list() -> str:
    return env.get_tr_id_order_list()


def get_tr_id_cancel_order() -> str:
    return env.get_tr_id_cancel_order()
