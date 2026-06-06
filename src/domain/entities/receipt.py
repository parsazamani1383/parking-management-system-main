from dataclasses import dataclass
from datetime import datetime
from src.domain.exceptions import ValidationError


@dataclass
class Receipt:
    id: int | None
    session_id: int
    receipt_number: str
    amount: float
    payment_method: str
    issued_at: datetime

    def __post_init__(self):
        if not self.receipt_number:
            raise ValidationError("Receipt number is required.")

        if self.amount < 0:
            raise ValidationError("Receipt amount cannot be negative.")

        if self.payment_method not in ("cash", "card", "online"):
            raise ValidationError(
                "Invalid payment method. Use cash, card or online."
            )

    def format_for_print(self) -> str:
        return (
            f"Receipt: {self.receipt_number} | "
            f"Amount: {self.amount} | "
            f"Date: {self.issued_at}"
        )