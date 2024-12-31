from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pymysql

from src.config import DB_URL


pymysql.install_as_MySQLdb()
engine = create_engine(DB_URL, echo=True)
SessionFactory = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
