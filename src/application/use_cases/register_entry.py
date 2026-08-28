from datetime import datetime

from src.domain.entities.parking_session import ParkingSession
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions import (
    ValidationError,
)

from src.application.interfaces.vehicle_repo import (
    VehicleRepository,
)
from src.application.interfaces.spot_repo import (
    SpotRepository,
)
from src.application.interfaces.session_repo import (
    SessionRepository,
)


class RegisterEntryUseCase:

    def __init__(
        self,
        vehicle_repo: VehicleRepository,
        spot_repo: SpotRepository,
        session_repo: SessionRepository,
    ):
        self._vehicle_repo = vehicle_repo
        self._spot_repo = spot_repo
        self._session_repo = session_repo

    def execute(
        self,
        plate_number: str,
        vehicle_type: str,
        shift_id: int,
    ) -> ParkingSession:

        vehicle = self._vehicle_repo.get_by_plate(
            plate_number
        )

        if vehicle is None:

            vehicle = Vehicle(
                id=None,
                plate_number=plate_number,
                vehicle_type=vehicle_type,
                color=None,
                brand=None,
                model=None,
                owner_name=None,
                owner_phone=None,
                created_at=datetime.now(),
            )

            vehicle = self._vehicle_repo.save(
                vehicle
            )

        active_session = (
            self._session_repo
            .get_active_by_vehicle(
                vehicle.id
            )
        )

        if active_session:

            raise ValidationError(
                "Vehicle already has an active session."
            )

        spot = (
            self._spot_repo
            .get_available_spot(
                vehicle.vehicle_type
            )
        )

        if spot is None:

            raise ValidationError(
                "No available parking spot."
            )

        spot.occupy()

        self._spot_repo.update(
            spot
        )

        session = ParkingSession(
            id=None,
            vehicle_id=vehicle.id,
            spot_id=spot.id,
            shift_id=shift_id,
            entry_time=datetime.now(),
        )

        return self._session_repo.save(
            session
        )