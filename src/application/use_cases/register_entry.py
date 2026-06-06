from datetime import datetime

from src.domain.entities.parking_session import ParkingSession
from src.domain.exceptions import (
    EntityNotFoundError,
    ValidationError,
    ParkingSpotUnavailableError
)

from src.application.interfaces.vehicle_repo import VehicleRepository
from src.application.interfaces.spot_repo import ParkingSpotRepository
from src.application.interfaces.session_repo import ParkingSessionRepository
from src.application.interfaces.shift_repo import OperatorShiftRepository


class RegisterVehicleEntryUseCase:

    def __init__(
        self,
        vehicle_repo: VehicleRepository,
        spot_repo: ParkingSpotRepository,
        session_repo: ParkingSessionRepository,
        shift_repo: OperatorShiftRepository
    ):
        self.vehicle_repo = vehicle_repo
        self.spot_repo = spot_repo
        self.session_repo = session_repo
        self.shift_repo = shift_repo

    def execute(self, plate_number: str, operator_user_id: int) -> ParkingSession:

        # 1. Find vehicle
        vehicle = self.vehicle_repo.get_by_plate(plate_number)
        if vehicle is None:
            raise EntityNotFoundError("Vehicle not found.")

        # 2. Check active session
        active_session = self.session_repo.get_active_by_vehicle(vehicle.id)
        if active_session is not None:
            raise ValidationError("Vehicle already has an active parking session.")

        # 3. Validate operator shift
        shift = self.shift_repo.get_active_shift(operator_user_id)
        if shift is None:
            raise ValidationError("Operator does not have an active shift.")

        # 4. Find available spot
        spot = self.spot_repo.find_available_spot(vehicle.vehicle_type)
        if spot is None:
            raise ParkingSpotUnavailableError("No available parking spot.")

        # 5. Occupy spot
        spot.occupy()

        # 6. Create session
        session = ParkingSession(
            id=None,
            vehicle_id=vehicle.id,
            spot_id=spot.id,
            shift_id=shift.id,
            entry_time=datetime.now(),
            exit_time=None,
            total_fee=None
        )

        # 7. Persist
        saved_session = self.session_repo.save(session)
        self.spot_repo.update(spot)

        return saved_session
