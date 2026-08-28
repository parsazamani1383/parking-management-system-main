from datetime import datetime

from src.domain.exceptions import ValidationError

from src.application.interfaces.vehicle_repo import (
    VehicleRepository,
)

from src.application.interfaces.session_repo import (
    SessionRepository,
)

from src.application.interfaces.spot_repo import (
    SpotRepository,
)

from src.application.interfaces.tariff_repo import (
    TariffRepository,
)

from src.application.services.fee_calculator import (
    FeeCalculator,
)


class RegisterExitUseCase:

    def __init__(
        self,
        vehicle_repo: VehicleRepository,
        session_repo: SessionRepository,
        spot_repo: SpotRepository,
        tariff_repo: TariffRepository,
        fee_calculator: FeeCalculator,
    ):
        self._vehicle_repo = vehicle_repo
        self._session_repo = session_repo
        self._spot_repo = spot_repo
        self._tariff_repo = tariff_repo
        self._fee_calculator = fee_calculator

    def execute(
        self,
        plate_number: str,
    ) -> float:

        vehicle = self._vehicle_repo.get_by_plate(
            plate_number
        )

        if vehicle is None:
            raise ValidationError(
                "Vehicle not found."
            )

        session = (
            self._session_repo
            .get_active_by_vehicle(
                vehicle.id
            )
        )

        if session is None:
            raise ValidationError(
                "No active session found."
            )

        spot = self._spot_repo.get_by_id(
            session.spot_id
        )

        tariff = (
            self._tariff_repo
            .get_active_tariff(
                vehicle.vehicle_type
            )
        )

        if tariff is None:
            raise ValidationError(
                "No active tariff found."
            )

        exit_time = datetime.now()

        fee = self._fee_calculator.calculate(
            session.entry_time,
            exit_time,
            tariff,
        )

        session.close(
            exit_time,
            fee,
        )

        self._session_repo.update(
            session
        )

        if spot:
            spot.release()
            self._spot_repo.update(
                spot
            )

        return fee