import pytest

from src.account.account import Account
from src.account.infra.account_repository import AccountRepository
from src.common.exception import InvestAppException
from src.common.type import BrokerType


@pytest.fixture
def sample_account():
    return Account(name="테스트 계좌", app_key="test_app_key", secret_key="test_secret_key", broker_type=BrokerType.UPBIT)


def test_save_account(account_repository: AccountRepository, sample_account: Account):
    saved_account = account_repository.save(sample_account)
    assert saved_account.id is not None

    # Then
    found_account = account_repository.find_by_id(saved_account.id)
    assert found_account is not None
    assert found_account.name == "테스트 계좌"
    assert found_account.app_key == "test_app_key"
    assert found_account.secret_key == "test_secret_key"
    assert found_account.broker_type.is_upbit()


def test_update_account(account_repository: AccountRepository, sample_account: Account):
    # Given
    saved_account = account_repository.save(sample_account)
    assert saved_account.broker_type.is_upbit()
    assert saved_account.id is not None

    # When
    saved_account.broker_type = BrokerType.KIS
    account_repository.update(saved_account.id, saved_account)

    # Then
    found_account = account_repository.find_by_id(saved_account.id)
    assert found_account.broker_type.is_kis()


def test_delete_account(account_repository: AccountRepository, sample_account: Account):
    # Given
    saved_account = account_repository.save(sample_account)
    assert saved_account.id is not None

    # When
    account_repository.delete_by_id(saved_account.id)

    # Then
    accounts = account_repository.find_all()
    assert len(accounts) == 0


def test_delete_account_not_found(account_repository: AccountRepository):
    # Given
    # When
    with pytest.raises(InvestAppException):
        account_repository.delete_by_id(1)


def test_find_all_accounts(account_repository: AccountRepository, sample_account: Account):
    # Given
    saved_account = account_repository.save(sample_account)
    assert saved_account.id is not None

    # When
    accounts = account_repository.find_all()
    assert len(accounts) == 1
