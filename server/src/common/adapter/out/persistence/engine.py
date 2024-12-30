from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import pymysql

from src.config import DB_URL


pymysql.install_as_MySQLdb()
engine = create_engine(DB_URL, echo=True)
SessionFactory = sessionmaker(bind=engine)


def get_session() -> Session:
    return SessionFactory()
