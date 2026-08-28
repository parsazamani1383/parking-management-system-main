from src.application.interfaces.spot_repo import SpotRepository


class DeleteParkingSpotUseCase:

    def __init__(
        self,
        repo: SpotRepository,
    ):
        self.repo = repo

    def execute(
        self,
        spot,
    ):

        if spot.status == "occupied":
            raise Exception(
                "امکان حذف جایگاه اشغال شده وجود ندارد."
            )

        self.repo.delete(
            spot.id
        )