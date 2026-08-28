from src.application.interfaces.tariff_repo import TariffRepository


class UpdateTariffUseCase:

    def __init__(
        self,
        tariff_repo: TariffRepository,
    ):
        self.tariff_repo = tariff_repo

    def execute(
            self,
            tariff,
            base_rate,
            hourly_rate,
            daily_rate,
    ):

        tariff.base_rate = float(base_rate)
        tariff.hourly_rate = float(hourly_rate)
        tariff.daily_rate = float(daily_rate)

        self.tariff_repo.update(
            tariff
        )