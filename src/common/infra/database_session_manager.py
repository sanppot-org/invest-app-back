from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session, sessionmaker


class DBSessionManager:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
