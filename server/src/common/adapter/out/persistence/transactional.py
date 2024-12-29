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
            # session을 현재 스레드에 바인딩
            Session.object_session = session
            try:
                result = func(*args, **kwargs)  # session 파라미터 제거
                return result
            finally:
                Session.object_session = None

    return wrapper
