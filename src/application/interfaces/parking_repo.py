from abc import ABC, abstractmethod
from src.domain.entities.parking import Parking


class ParkingRepository(ABC):

    @abstractmethod
    def get_by_id(
        self,
        parking_id: int
    ) -> Parking | None:
        pass

    @abstractmethod
    def get_current(self) -> Parking | None:
        pass