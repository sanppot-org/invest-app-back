from typing import List
from sqlalchemy import JSON, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from domain.stock_info import StockInfo
from infra import engine
from sqlalchemy import func
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column
from infra.model import Interval


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


class IntervalType(TypeDecorator):
    impl = JSON

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.to_dict()
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return Interval(**value)
        return None


class BaseEntity(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[str] = mapped_column(
        sqlite.DATETIME,
        server_default=func.now(),  # INSERT 시 서버에서 시간 생성
        nullable=False,
    )
    updated_at: Mapped[str] = mapped_column(
        sqlite.DATETIME,
        server_default=func.now(),  # INSERT 시 서버에서 시간 생성
        onupdate=func.now(),  # UPDATE 시 자동 업데이트
        nullable=False,
    )


class Strategy(BaseEntity):
    __tablename__ = "starategy"
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30), index=True)
    invest_rate: Mapped[float] = mapped_column(sqlite.FLOAT)
    env: Mapped[str] = mapped_column(sqlite.CHAR(1), default="R")
    stocks: Mapped[List[StockInfo]] = mapped_column(StockInfoList, nullable=True)
    interval: Mapped[Interval] = mapped_column(IntervalType)
    last_run: Mapped[str] = mapped_column(sqlite.DATETIME, nullable=True)


class Account(BaseEntity):
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
