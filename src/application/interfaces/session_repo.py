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

    @abstractmethod
    def get_all(
            self
    ) -> list[ParkingSession]:
        pass

    @abstractmethod
    def get_recent_sessions(
            self,
            limit: int = 10
    ) -> list[dict]:
        pass


    @abstractmethod
    def search_active_vehicles(
            self,
            plate_part: str
    ) -> list[dict]:
        pass

    @abstractmethod
    def get_active_session_info(
            self,
            session_id: int
    ) -> dict | None:
        pass

    @abstractmethod
    def get_daily_revenue(
            self,
            days: int,
    ) -> list[dict]:
        pass

    @abstractmethod
    def get_all(
            self
    ) -> list[ParkingSession]:
        pass

    @abstractmethod
    def get_recent_sessions(
            self,
            limit: int = 10
    ) -> list[dict]:
        pass


    @abstractmethod
    def search_active_vehicles(
            self,
            plate_part: str
    ) -> list[dict]:
        pass

    @abstractmethod
    def get_active_session_info(
            self,
            session_id: int
    ) -> dict | None:
        pass

    @abstractmethod
    def get_daily_revenue(
            self,
            days: int,
    ) -> list[dict]:
        pass
