from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import DB_URL


engine = create_engine(DB_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    return SessionFactory()
