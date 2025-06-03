import pytest
import sqlalchemy

from src.common.infra.base_entity import BaseEntity
from src.config.containers import Container

TEST_DB_URL = "mysql+pymysql://root:1234@localhost:3310/invest?charset=utf8"


@pytest.fixture(scope="function")
def test_db_engine():
    engine = sqlalchemy.create_engine(url=TEST_DB_URL, echo=True)
    BaseEntity.metadata.create_all(engine)
    with engine.connect() as connection:
        transaction = connection.begin()
        yield connection
        if transaction.is_active:
            transaction.rollback()


@pytest.fixture
def container(test_db_engine):
    container: Container = Container()
    container.config.DB_URL.from_value(TEST_DB_URL)
    container.engine.override(test_db_engine)
    return container


@pytest.fixture
def account_repository(container: Container):
    return container.account_repository()
