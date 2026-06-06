from abc import ABC, abstractmethod
from src.domain.entities.vehicle import Vehicle


class VehicleRepository(ABC):

    @abstractmethod
    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        pass

    @abstractmethod
    def get_by_plate(self, plate_number: str) -> Vehicle | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Vehicle]:
        pass

    @abstractmethod
    def save(self, vehicle: Vehicle) -> Vehicle:
        pass

    @abstractmethod
    def update(self, vehicle: Vehicle) -> None:
        pass