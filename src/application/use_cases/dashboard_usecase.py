from datetime import date

from src.application.interfaces.spot_repo import (
    SpotRepository,
)

from src.application.interfaces.receipt_repo import (
    ReceiptRepository,
)

from src.application.interfaces.session_repo import (
    SessionRepository,
)


class DashboardUseCase:

    def __init__(
        self,
        spot_repo: SpotRepository,
        session_repo: SessionRepository,
        receipt_repo: ReceiptRepository,
    ):
        self._spot_repo = spot_repo
        self._session_repo = session_repo
        self._receipt_repo = receipt_repo

    def execute(self) -> dict:

        spots = self._spot_repo.get_all()

        total_capacity = len(spots)

        occupied_count = sum(
            1
            for spot in spots
            if spot.status == "occupied"
        )

        available_count = sum(
            1
            for spot in spots
            if spot.status == "available"
        )

        receipts = self._receipt_repo.get_all()

        today = date.today()

        today_revenue = sum(
            receipt.amount
            for receipt in receipts
            if receipt.issued_at.date() == today
        )

        recent_sessions = (
            self._session_repo
            .get_recent_sessions(10)
        )

        return {
            "total_capacity": total_capacity,
            "occupied_count": occupied_count,
            "available_count": available_count,
            "today_revenue": today_revenue,
            "recent_sessions": recent_sessions,
        }