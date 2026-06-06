from abc import ABC, abstractmethod
from src.domain.entities.operator_shift import OperatorShift


class ShiftRepository(ABC):

    @abstractmethod
    def get_active_shift(
        self,
        user_id: int
    ) -> OperatorShift | None:
        pass

    @abstractmethod
    def save(
        self,
        shift: OperatorShift
    ) -> OperatorShift:
        pass

    @abstractmethod
    def update(
        self,
        shift: OperatorShift
    ) -> None:
        pass