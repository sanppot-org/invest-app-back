from typing import Generic, List, Type, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.exception import ExeptionType, InvestAppException
from src.common.infra.type import E


class SqlalchemyRepository(Generic[E]):
    def __init__(self, entity_type: Type[E]):
        self.entity_type = entity_type

    def save(self, entity: E, session: Session) -> E:
        if entity.id:
            session.merge(entity)
        else:
            session.add(entity)
        session.flush()
        return entity

    def delete_by_id(self, id: int, session: Session) -> int:
        entity = session.query(self.entity_type).filter(self.entity_type.id == id).first()
        if entity:
            session.delete(entity)
            session.flush()
            return id
        raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id=id)

    def find_all(self, session: Session) -> List[E]:
        stmt = select(self.entity_type)
        return list(session.scalars(stmt).all())

    def find_by_id(self, id: int, session: Session) -> Optional[E]:
        stmt = select(self.entity_type).where(self.entity_type.id == id).execution_options(populate_existing=True)
        return session.scalars(stmt).one_or_none()
