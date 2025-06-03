# Define type variables
from typing import TypeVar

from src.common.domain_model import DomainModel
from src.common.infra.base_entity import BaseEntity

D = TypeVar("D", bound=DomainModel)  # Domain model type
E = TypeVar("E", bound=BaseEntity)  # Entity type bound to BaseEntity
