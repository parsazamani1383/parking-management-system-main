from abc import ABC, abstractmethod
from src.domain.entities.parking_session import ParkingSession


class SessionRepository(ABC):

    @abstractmethod
    def get_by_id(
        self,
        session_id: int
    ) -> ParkingSession | None:
        pass

    @abstractmethod
    def get_active_by_vehicle(
        self,
        vehicle_id: int
    ) -> ParkingSession | None:
        pass

    @abstractmethod
    def get_active_sessions(
        self
    ) -> list[ParkingSession]:
        pass

    @abstractmethod
    def save(
        self,
        session: ParkingSession
    ) -> ParkingSession:
        pass

    @abstractmethod
    def update(
        self,
        session: ParkingSession
    ) -> None:
        pass