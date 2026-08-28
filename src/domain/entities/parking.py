from dataclasses import dataclass
from datetime import datetime

from src.domain.exceptions import ValidationError


@dataclass
class Parking:
    id: int | None
    name: str
    code: str
    status: str
    created_at: datetime
    updated_at: datetime | None = None

    def __post_init__(self):

        if not self.name:
            raise ValidationError(
                "Parking name cannot be empty."
            )

        if not self.code:
            raise ValidationError(
                "Parking code cannot be empty."
            )

        if self.status not in (
            "active",
            "inactive",
            "maintenance",
        ):
            raise ValidationError(
                "Invalid parking status."
            )

    # ---------- Business Logic ----------

    def activate(self):
        self.status = "active"
        self.updated_at = datetime.now()

    def deactivate(self):
        self.status = "inactive"
        self.updated_at = datetime.now()

    def set_maintenance(self):
        self.status = "maintenance"
        self.updated_at = datetime.now()

    @property
    def is_active(self) -> bool:
        return self.status == "active"