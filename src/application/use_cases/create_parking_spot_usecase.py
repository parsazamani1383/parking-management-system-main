from src.domain.entities.parking_spot import ParkingSpot
from src.application.interfaces.spot_repo import SpotRepository


class CreateParkingSpotUseCase:

    def __init__(
        self,
        repo: SpotRepository,
    ):
        self.repo = repo

    def execute(
            self,
            spot_number,
            spot_type,
            level_label,
            section_label,
    ):

        if self.repo.get_by_number(spot_number):

            raise Exception(
                "شماره جایگاه تکراری است."
            )

        spot = ParkingSpot(
            id=None,
            parking_id=1,
            spot_number=spot_number,
            spot_type=spot_type,
            status="available",
            level_label=level_label,
            section_label=section_label,
            is_active=True,
        )

        return self.repo.save(spot)