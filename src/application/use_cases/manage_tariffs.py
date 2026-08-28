from src.application.interfaces.tariff_repo import (
    TariffRepository,
)


class ManageTariffsUseCase:

    def __init__(
        self,
        tariff_repo: TariffRepository,
    ):
        self._tariff_repo = tariff_repo

    def get_tariff(
        self,
        vehicle_type: str,
    ):

        return (
            self._tariff_repo
            .get_active_tariff(
                vehicle_type
            )
        )

    def update_hourly_rate(
        self,
        tariff_id: int,
        new_rate: float,
    ):

        tariff = (
            self._tariff_repo
            .get_by_id(
                tariff_id
            )
        )

        tariff.hourly_rate = new_rate

        self._tariff_repo.update(
            tariff
        )

        return tariff

    def update_base_rate(
        self,
        tariff_id: int,
        new_rate: float,
    ):

        tariff = (
            self._tariff_repo
            .get_by_id(
                tariff_id
            )
        )

        tariff.base_rate = new_rate

        self._tariff_repo.update(
            tariff
        )

        return tariff