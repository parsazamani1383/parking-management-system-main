from src.application.interfaces.session_repo import (
    SessionRepository,
)

from src.application.interfaces.vehicle_repo import (
    VehicleRepository,
)


class ListActiveVehiclesUseCase:

    def __init__(
        self,
        session_repo: SessionRepository,
        vehicle_repo: VehicleRepository,
    ):
        self._session_repo = session_repo
        self._vehicle_repo = vehicle_repo

    def execute(self) -> list[dict]:

        result = []

        sessions = (
            self._session_repo
            .get_active_sessions()
        )

        for session in sessions:

            vehicle = (
                self._vehicle_repo
                .get_by_id(
                    session.vehicle_id
                )
            )

            result.append(
                {
                    "session_id": session.id,
                    "plate_number": vehicle.plate_number,
                    "vehicle_type": vehicle.vehicle_type,
                    "entry_time": session.entry_time,
                    "spot_id": session.spot_id,
                }
            )

        return result