from src.application.interfaces.spot_repo import SpotRepository


class UpdateParkingSpotUseCase:

    def __init__(
        self,
        repo: SpotRepository,
    ):
        self.repo = repo

    def execute(
        self,
        spot,
        spot_number,
        spot_type,
        level_label,
        section_label,
        is_active,
    ):

        duplicate = self.repo.get_by_number(
            spot_number
        )

        if (
            duplicate is not None
            and duplicate.id != spot.id
        ):
            raise Exception(
                "شماره جایگاه تکراری است."
            )

        spot.spot_number = spot_number
        spot.spot_type = spot_type
        spot.level_label = level_label
        spot.section_label = section_label
        spot.is_active = is_active

        self.repo.update(spot)