from typing import List
from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from domain.stock_info import StockInfo
from infra import engine
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class StockInfoList(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        if value is not None:
            return [stock.to_dict() for stock in value]
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return [StockInfo(**stock) for stock in value]
        return None


class Strategy(Base):
    __tablename__ = "starategy"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30), index=True)
    invest_rate: Mapped[float] = mapped_column(sqlite.FLOAT)
    env: Mapped[str] = mapped_column(sqlite.CHAR(1), default="R")
    stocks: Mapped[List[StockInfo]] = mapped_column(StockInfoList, nullable=True)


class Account(Base):
    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30))
    number: Mapped[str] = mapped_column(sqlite.VARCHAR(10), index=True)
    product_code: Mapped[str] = mapped_column(sqlite.CHAR(2))
    app_key: Mapped[str] = mapped_column(sqlite.VARCHAR(50))
    secret_key: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    url_base: Mapped[str] = mapped_column(sqlite.VARCHAR(100))
    token: Mapped[str] = mapped_column(sqlite.VARCHAR(200), nullable=True)


Base.metadata.create_all(bind=engine.engine)
