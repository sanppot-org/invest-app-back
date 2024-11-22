from sqlalchemy.ext.declarative import declarative_base
from infra import engine
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Strategy(Base):
    __tablename__ = "starategy"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlite.VARCHAR(30), index=True)
    invest_rate: Mapped[float] = mapped_column(sqlite.FLOAT)
    env: Mapped[str] = mapped_column(sqlite.CHAR(1), default="R")


Base.metadata.create_all(bind=engine.engine)
