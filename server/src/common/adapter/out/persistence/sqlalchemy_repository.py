from typing import Generic, List, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.adapter.out.persistence.base_entity import BaseEntity
from src.common.domain.exception import ExeptionType, InvestAppException

Entity = TypeVar("Entity", bound=BaseEntity)


class SqlalchemyRepository(Generic[Entity]):
    def __init__(self, session: Session, entity_type: Type[Entity]):
        self.session = session
        self.entity_type = entity_type

    def save(self, entity: Entity) -> Entity:
        with self.session as session:
            if entity.id is None:
                session.add(entity)
            else:
                session.merge(entity)
            session.commit()
            return entity

    def find_by_id(self, id: int) -> Entity | None:
        with self.session as session:
            stmt = select(self.entity_type).where(self.entity_type.id == id)
            return session.scalars(stmt).one_or_none()

    def find_all(self) -> List[Entity]:
        with self.session as session:
            stmt = select(self.entity_type)
            return list(session.scalars(stmt).all())

    def delete_by_id(self, id: int) -> int:
        with self.session as session:
            entity = session.query(self.entity_type).filter(self.entity_type.id == id).first()

            if not entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

            session.delete(entity)
            session.commit()
            return id
