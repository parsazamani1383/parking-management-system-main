from abc import ABC, abstractmethod
from src.domain.entities.receipt import Receipt


class ReceiptRepository(ABC):

    @abstractmethod
    def get_by_id(
        self,
        receipt_id: int
    ) -> Receipt | None:
        pass

    @abstractmethod
    def get_by_session(
        self,
        session_id: int
    ) -> Receipt | None:
        pass

    @abstractmethod
    def save(
        self,
        receipt: Receipt
    ) -> Receipt:
        pass