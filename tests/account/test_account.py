import pytest
from account.account import Account
from common.type import BrokerType


def test_account_creation_success():
    # 모든 필수 필드가 제공된 경우
    account = Account(
        name="테스트 계좌",
        app_key="test_app_key",
        secret_key="test_secret_key",
        broker_type=BrokerType.UPBIT,
    )
    assert account.name == "테스트 계좌"
    assert account.app_key == "test_app_key"
    assert account.secret_key == "test_secret_key"
    assert account.broker_type == BrokerType.UPBIT


def test_account_creation_failure():
    # name이 누락된 경우
    with pytest.raises(AssertionError, match="필수 필드가 누락되었습니다"):
        Account(
            name="",
            app_key="test_app_key",
            secret_key="test_secret_key",
            broker_type=BrokerType.UPBIT,
        )

    # app_key가 누락된 경우
    with pytest.raises(AssertionError, match="필수 필드가 누락되었습니다"):
        Account(
            name="테스트 계좌",
            app_key="",
            secret_key="test_secret_key",
            broker_type=BrokerType.UPBIT,
        )

    # secret_key가 누락된 경우
    with pytest.raises(AssertionError, match="필수 필드가 누락되었습니다"):
        Account(
            name="테스트 계좌",
            app_key="test_app_key",
            secret_key="",
            broker_type=BrokerType.UPBIT,
        )

    # broker_type이 누락된 경우
    with pytest.raises(AssertionError, match="필수 필드가 누락되었습니다"):
        Account(
            name="테스트 계좌",
            app_key="test_app_key",
            secret_key="test_secret_key",
            broker_type=None,
        )
