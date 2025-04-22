from typing import Generic, List, Type, TypeVar, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from common.exception import ExeptionType, InvestAppException
from db.base_entity import BaseEntity


Entity = TypeVar("Entity", bound=BaseEntity)


class SqlalchemyRepository(Generic[Entity]):
    def __init__(self, entity_type: Type[Entity]):
        self.entity_type = entity_type

    def save(self, entity: Entity, session: Session) -> Entity:
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
        raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

    def find_all(self, session: Session) -> List[Entity]:
        stmt = select(self.entity_type)
        return list(session.scalars(stmt).all())

    def find_by_id(self, id: int, session: Session) -> Optional[Entity]:
        stmt = select(self.entity_type).where(self.entity_type.id == id).execution_options(populate_existing=True)
        return session.scalars(stmt).one_or_none()
