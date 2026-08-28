from abc import ABC, abstractmethod
from src.domain.entities.parking_spot import ParkingSpot


class SpotRepository(ABC):

    @abstractmethod
    def get_by_id(self, spot_id: int) -> ParkingSpot | None:
        pass

    @abstractmethod
    def get_available_spot(
        self,
        spot_type: str,
    ) -> ParkingSpot | None:
        pass

    @abstractmethod
    def get_all(self) -> list[ParkingSpot]:
        pass

    @abstractmethod
    def save(self, spot: ParkingSpot) -> ParkingSpot:
        pass

    @abstractmethod
    def update(self, spot: ParkingSpot) -> None:
        pass

    @abstractmethod
    def delete(
            self,
            spot_id: int,
    ) -> None:
        pass

    @abstractmethod
    def get_by_number(
            self,
            spot_number: str,
    ) -> ParkingSpot | None:
        pass
