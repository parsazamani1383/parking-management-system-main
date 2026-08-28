from src.application.interfaces.session_repo import (
    SessionRepository,
)

from src.application.interfaces.spot_repo import (
    SpotRepository,
)

from src.application.interfaces.receipt_repo import (
    ReceiptRepository,
)


class ReportsUseCase:

    def __init__(
        self,
        session_repo: SessionRepository,
        spot_repo: SpotRepository,
        receipt_repo: ReceiptRepository,
    ):
        self._session_repo = session_repo
        self._spot_repo = spot_repo
        self._receipt_repo = receipt_repo

    def parking_status(self) -> dict:

        spots = self._spot_repo.get_all()

        total_spots = len(spots)

        available_spots = sum(
            1
            for spot in spots
            if spot.status == "available"
        )

        occupied_spots = sum(
            1
            for spot in spots
            if spot.status == "occupied"
        )

        reserved_spots = sum(
            1
            for spot in spots
            if spot.status == "reserved"
        )

        return {
            "total_spots": total_spots,
            "available_spots": available_spots,
            "occupied_spots": occupied_spots,
            "reserved_spots": reserved_spots,
        }

    def session_summary(self) -> dict:

        sessions = self._session_repo.get_all()

        total_sessions = len(sessions)

        active_sessions = sum(
            1
            for session in sessions
            if session.is_active
        )

        completed_sessions = (
            total_sessions - active_sessions
        )

        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "completed_sessions": completed_sessions,
        }

    def revenue_summary(self) -> dict:

        receipts = self._receipt_repo.get_all()

        total_receipts = len(receipts)

        total_revenue = sum(
            receipt.amount
            for receipt in receipts
        )

        average_revenue = (
            total_revenue / total_receipts
            if total_receipts > 0
            else 0
        )

        return {
            "total_receipts": total_receipts,
            "total_revenue": total_revenue,
            "average_revenue": average_revenue,
        }

    def full_report(self) -> dict:

        return {
            "parking": self.parking_status(),
            "sessions": self.session_summary(),
            "revenue": self.revenue_summary(),
        }

    def daily_revenue_report(
            self,
            days: int,
    ):
        return self._session_repo.get_daily_revenue(
            days
        )