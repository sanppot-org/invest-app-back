from typing import List
from contextlib import contextmanager
from infra import engine
from infra.schema import Strategy


@contextmanager
def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save(strategy: Strategy) -> Strategy:
    with get_db() as db:
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        return strategy


def find_all() -> List[Strategy]:
    with get_db() as db:
        return db.query(Strategy).all()
