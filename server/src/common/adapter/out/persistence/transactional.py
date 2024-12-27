from functools import wraps
from sqlalchemy.orm import Session
from contextlib import contextmanager


@contextmanager
def transactional_context():
    session = Session()  # 세션 팩토리에서 세션 생성
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transactional_context() as session:
            return func(*args, session=session, **kwargs)

    return wrapper
