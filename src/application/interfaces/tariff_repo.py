from abc import ABC, abstractmethod
from src.domain.entities.tariff import Tariff


class TariffRepository(ABC):

    @abstractmethod
    def get_active_tariff(
        self,
        vehicle_type: str
    ) -> Tariff | None:
        pass

    @abstractmethod
    def get_by_id(
        self,
        tariff_id: int
    ) -> Tariff | None:
        pass

    @abstractmethod
    def save(
        self,
        tariff: Tariff
    ) -> Tariff:
        pass

    @abstractmethod
    def update(
        self,
        tariff: Tariff
    ) -> None:
        pass