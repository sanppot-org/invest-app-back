from typing import List, Optional, Generic

from src.common.exception import ExeptionType, InvestAppException
from src.common.infra.database_session_manager import DBSessionManager
from src.common.infra.entity_mapper import EntityMapper
from src.common.infra.sqlalchemy_repository import SqlalchemyRepository
from src.common.infra.type import D, E


class GenericRepository(Generic[D, E]):
    def __init__(
            self,
            mapper: EntityMapper[D, E],
            repository: SqlalchemyRepository[E],
            session_manager: DBSessionManager,
    ):
        self.repository = repository
        self.mapper = mapper
        self.session_manager = session_manager

    def save(self, domain_object: D) -> D:
        with self.session_manager.session() as session:
            entity = self.mapper.to_entity(domain_object)
            saved_entity = self.repository.save(entity, session)
            return self.mapper.to_domain(saved_entity)

    def update(self, id: int, domain_object: D) -> D:
        with self.session_manager.session() as session:
            found_entity: Optional[E] = self.repository.find_by_id(id, session)
            if not found_entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id=id)
            found_entity.update(self.mapper.to_entity(domain_object))
            return self.mapper.to_domain(found_entity)

    def delete_by_id(self, id: int) -> int:
        with self.session_manager.session() as session:
            return self.repository.delete_by_id(id, session)

    def find_by_id(self, id: int) -> D:
        with self.session_manager.session() as session:
            found_entity = self.repository.find_by_id(id, session)
            if not found_entity:
                raise InvestAppException(ExeptionType.ENTITY_NOT_FOUND, id=id)
            return self.mapper.to_domain(found_entity)

    def find_all(self) -> List[D]:
        with self.session_manager.session() as session:
            entities = self.repository.find_all(session)
            return [self.mapper.to_domain(entity) for entity in entities]
