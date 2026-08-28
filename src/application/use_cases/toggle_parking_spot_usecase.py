from src.application.interfaces.spot_repo import SpotRepository


class ToggleParkingSpotUseCase:

    def __init__(
        self,
        repo: SpotRepository,
    ):
        self.repo = repo

    def execute(
        self,
        spot,
    ):

        spot.is_active = not spot.is_active

        self.repo.update(
            spot
        )
