from dataclasses import dataclass
from datetime import datetime
from src.domain.exceptions import ValidationError

@dataclass
class OperatorShift:
    id: int | None
    user_id: int
    start_time: datetime
    end_time: datetime | None = None

    def __post_init__(self):
        if not self.start_time:
            raise ValidationError("Start time is required.")

    # -------- Business Logic --------

    def close(self, end_time: datetime):
        if self.end_time is not None:
            raise ValidationError("Shift is already closed.")

        if end_time <= self.start_time:
            raise ValidationError("Shift end time must be after start time.")

        self.end_time = end_time

    @property
    def is_active(self) -> bool:
        return self.end_time is None
