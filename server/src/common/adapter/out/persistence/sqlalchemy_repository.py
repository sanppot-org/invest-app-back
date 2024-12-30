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
            if entity.id:
                session.merge(entity)
            else:
                session.add(entity)
            session.commit()
        return entity

    def delete_by_id(self, id: int) -> int:
        entity = self.session.query(self.entity_type).filter(self.entity_type.id == id).first()

        if entity:
            self.session.delete(entity)
            self.session.commit()
            return id

        raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

    def find_all(self) -> List[Entity]:
        stmt = select(self.entity_type)
        return [entity for entity in self.session.scalars(stmt).all()]

    def find_by_id(self, id: int) -> Entity:
        stmt = select(self.entity_type).where(self.entity_type.id == id).execution_options(populate_existing=True)
        entity = self.session.scalars(stmt).one_or_none()

        if not entity:
            raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

        return entity
