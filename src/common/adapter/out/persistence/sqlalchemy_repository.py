from typing import Generic, List, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.common.adapter.out.persistence.base_entity import BaseEntity
from src.common.adapter.out.persistence.engine import session_scope
from src.common.domain.exception import ExeptionType, InvestAppException


Entity = TypeVar("Entity", bound=BaseEntity)


class SqlalchemyRepository(Generic[Entity]):
    def __init__(self, entity_type: Type[Entity]):
        self.entity_type = entity_type

    def save(self, entity: Entity, session: Session | None = None) -> Entity:
        if session:
            return self._save(entity, session)

        with session_scope() as session:
            return self._save(entity, session)

    def _save(self, entity: Entity, session: Session) -> Entity:
        if entity.id:
            session.merge(entity)
        else:
            session.add(entity)
        session.commit()
        return entity

    def delete_by_id(self, id: int) -> int:
        with session_scope() as session:
            entity = session.query(self.entity_type).filter(self.entity_type.id == id).first()

        if entity:
            session.delete(entity)
            session.commit()
            return id

        raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

    def find_all(self, session: Session | None = None) -> List[Entity]:
        if session:
            return self._find_all(session)

        with session_scope() as session:
            return self._find_all(session)

    def _find_all(self, session: Session) -> List[Entity]:
        stmt = select(self.entity_type)
        return list(session.scalars(stmt).all())

    def find_by_id(self, id: int, session: Session | None = None) -> Entity:
        if session:
            return self._find_by_id(id, session)

        with session_scope() as session:
            return self._find_by_id(id, session)

    def _find_by_id(self, id: int, session: Session) -> Entity:
        stmt = select(self.entity_type).where(self.entity_type.id == id).execution_options(populate_existing=True)
        entity = session.scalars(stmt).one_or_none()

        if not entity:
            raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

        return entity
