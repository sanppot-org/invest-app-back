from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from src.common.domain.logging_config import logger


@dataclass
class ConditionResult:
    is_satisfied: bool
    details: Dict[str, Any]

    def __str__(self) -> str:
        result_str = "만족" if self.is_satisfied else "불만족"
        details_str = ", ".join(f"{k}: {v}" for k, v in self.details.items())
        return f"{result_str} ({details_str})"


class StrategyCondition(ABC):
    def __init__(self):
        self._next_condition: Optional[StrategyCondition] = None

    def set_next(self, condition: "StrategyCondition") -> "StrategyCondition":
        self._next_condition = condition
        return condition

    def check_chain(self) -> bool:
        result = self.check()
        logger.info(f"{self.name}: {result}")

        if not result.is_satisfied:
            return False

        if self._next_condition:
            return self._next_condition.check_chain()

        return True

    @abstractmethod
    def check(self) -> ConditionResult:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class CompositeCondition(StrategyCondition):
    def __init__(self, conditions: List[StrategyCondition], operator: str = "AND"):
        super().__init__()
        self.conditions = conditions
        self.operator = operator

    @property
    def name(self) -> str:
        return f"{self.operator} 그룹"

    def check(self) -> ConditionResult:
        results = [condition.check() for condition in self.conditions]

        if self.operator == "AND":
            is_satisfied = all(r.is_satisfied for r in results)
        else:  # OR
            is_satisfied = any(r.is_satisfied for r in results)

        details = {"조건 수": len(results), "만족 수": sum(1 for r in results if r.is_satisfied)}

        return ConditionResult(is_satisfied, details)
