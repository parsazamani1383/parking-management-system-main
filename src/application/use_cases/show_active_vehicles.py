from src.application.interfaces.session_repo import (
    SessionRepository,
)


class ShowActiveVehiclesUseCase:

    def __init__(
        self,
        session_repo: SessionRepository,
    ):
        self._session_repo = session_repo

    def execute(
        self,
        plate_filter: str = "",
    ):

        return self._session_repo.search_active_vehicles(
            plate_filter
        )