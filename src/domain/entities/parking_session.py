from dataclasses import dataclass
from datetime import datetime
from src.domain.exceptions import ValidationError, SessionAlreadyClosedError

@dataclass
class ParkingSession:
    id: int | None
    vehicle_id: int
    spot_id: int
    shift_id: int
    entry_time: datetime
    exit_time: datetime | None = None
    total_fee: float | None = None

    def __post_init__(self):
        if self.entry_time > datetime.now():
            raise ValidationError("Entry time cannot be in the future.")

    # -------- Business Logic --------

    def close(self, exit_time: datetime, fee: float):
        if self.exit_time is not None:
            raise SessionAlreadyClosedError("This session is already closed.")

        if exit_time <= self.entry_time:
            raise ValidationError("Exit time must be after entry time.")

        if fee < 0:
            raise ValidationError("Fee cannot be negative.")

        self.exit_time = exit_time
        self.total_fee = fee

    @property
    def is_active(self) -> bool:
        return self.exit_time is None
