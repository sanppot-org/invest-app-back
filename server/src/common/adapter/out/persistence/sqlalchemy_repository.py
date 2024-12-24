from typing import Generic, List, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.common.adapter.out.persistence.base_entity import BaseEntity
from src.common.domain.base_domain_model import BaseDomainModel
from src.common.domain.exception import ExeptionType, InvestAppException
from src.common.application.port.out.repository import Repository
from src.common.adapter.out.persistence.entity_mapper import EntityMapper


E = TypeVar("E", bound=BaseEntity)
M = TypeVar("M", bound=BaseDomainModel)


class SqlalchemyRepository(Repository[M], Generic[E, M]):
    def __init__(self, session: Session, mapper: EntityMapper[E, M], entity_type: Type[E]):
        self.session = session
        self.mapper = mapper
        self.entity_type = entity_type

    def save(self, model: M) -> M:
        with self.session as session:
            entity = self.mapper.to_entity(model)
            session.add(entity)
            session.commit()
            return self.mapper.to_model(entity)

    def update(self, id: int, model: M) -> M:
        with self.session as session:
            entity = session.query(self.entity_type).filter(self.entity_type.id == id).first()
            if not entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

            for key, value in model.get_update_fields().items():
                setattr(entity, key, value)

            session.commit()
            return self.mapper.to_model(entity)

    def delete_by_id(self, id: int) -> int:
        with self.session as session:
            entity = session.query(self.entity_type).filter(self.entity_type.id == id).first()
            if entity:
                session.delete(entity)
                session.commit()
                return id
            raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)

    def find_all(self) -> List[M]:
        with self.session as session:
            stmt = select(self.entity_type)
            return [self.mapper.to_model(entity) for entity in session.scalars(stmt).all()]

    def find_by_id(self, id: int) -> M | None:
        with self.session as session:
            stmt = select(self.entity_type).where(self.entity_type.id == id)
            entity = session.scalars(stmt).one_or_none()
            if not entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id)
            return self.mapper.to_model(entity)
