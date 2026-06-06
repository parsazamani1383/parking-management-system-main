from dataclasses import dataclass
from datetime import datetime
from src.domain.exceptions import ValidationError


@dataclass
class Vehicle:
    id: int | None
    plate_number: str
    vehicle_type: str
    color: str | None
    brand: str | None
    model: str | None
    owner_name: str | None
    owner_phone: str | None
    created_at: datetime
    updated_at: datetime | None = None

    def __post_init__(self):
        if not self.plate_number:
            raise ValidationError("Plate number cannot be empty.")

        if self.vehicle_type not in ("car", "motorcycle"):
            raise ValidationError("Invalid vehicle type.")

    # ---- Business Behavior ----

    def is_car(self) -> bool:
        return self.vehicle_type == "car"

    def is_motorcycle(self) -> bool:
        return self.vehicle_type == "motorcycle"

    def update_owner(self, name: str, phone: str):
        if not name:
            raise ValidationError("Owner name cannot be empty.")

        self.owner_name = name
        self.owner_phone = phone
        self.updated_at = datetime.now()
