from datetime import datetime

from src.domain.entities.receipt import Receipt
from src.domain.exceptions import ValidationError

from src.application.interfaces.session_repo import (
    SessionRepository,
)

from src.application.interfaces.receipt_repo import (
    ReceiptRepository,
)


class IssueReceiptUseCase:

    def __init__(
        self,
        session_repo: SessionRepository,
        receipt_repo: ReceiptRepository,
    ):
        self._session_repo = session_repo
        self._receipt_repo = receipt_repo

    def execute(
        self,
        session_id: int,
        payment_method: str,
    ) -> Receipt:

        session = self._session_repo.get_by_id(
            session_id
        )

        if session is None:
            raise ValidationError(
                "Session not found."
            )

        if session.is_active:
            raise ValidationError(
                "Session is still active."
            )

        existing_receipt = (
            self._receipt_repo.get_by_session(
                session_id
            )
        )

        if existing_receipt:
            raise ValidationError(
                "Receipt already exists."
            )

        receipt = Receipt(
            id=None,
            session_id=session.id,
            receipt_number=(
                f"RCP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            ),
            amount=session.total_fee,
            payment_method=payment_method,
            issued_at=datetime.now(),
        )

        return self._receipt_repo.save(
            receipt
        )