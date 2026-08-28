from src.application.interfaces.user_repo import UserRepository
from src.application.interfaces.spot_repo import SpotRepository
from src.application.interfaces.tariff_repo import TariffRepository


class AdminPanelUseCase:

    def __init__(
        self,
        user_repo: UserRepository,
        spot_repo: SpotRepository,
        tariff_repo: TariffRepository,
    ):
        self.user_repo = user_repo
        self.spot_repo = spot_repo
        self.tariff_repo = tariff_repo

    def execute(self):

        users = self.user_repo.list_all()

        spots = self.spot_repo.get_all()

        car_tariff = self.tariff_repo.get_active_tariff("car")

        motorcycle_tariff = self.tariff_repo.get_active_tariff("motorcycle")

        return {
            "users": users,
            "spots": spots,
            "car_tariff": car_tariff,
            "motorcycle_tariff": motorcycle_tariff,
        }
