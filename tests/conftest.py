import pytest
from sqlalchemy import create_engine
from src.config.containers import Container
from src.db.base_entity import BaseEntity

TEST_DB_URL = "mysql+pymysql://root:1234@localhost:3306/invest"


@pytest.fixture(scope="function")
def test_db_engine():
    engine = create_engine(url=TEST_DB_URL, echo=True)
    BaseEntity.metadata.create_all(engine)
    with engine.connect() as connection:
        transaction = connection.begin()
        yield connection
        if transaction.is_active:
            transaction.rollback()


@pytest.fixture
def container(test_db_engine):
    container: Container = Container()
    container.engine.override(test_db_engine)
    return container


@pytest.fixture
def account_service(container: Container):
    return container.account_service()
