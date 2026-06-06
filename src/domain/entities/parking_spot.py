from dataclasses import dataclass
from src.domain.exceptions import (
    ValidationError,
    ParkingSpotUnavailableError,
)


@dataclass
class ParkingSpot:
    id: int | None
    parking_id: int
    spot_number: str
    spot_type: str
    status: str
    level_label: str | None = None
    section_label: str | None = None
    is_active: bool = True

    def __post_init__(self):

        if self.spot_type not in (
            "car",
            "motorcycle",
            "disabled",
            "vip",
        ):
            raise ValidationError(
                "Invalid parking spot type."
            )

        if self.status not in (
            "available",
            "occupied",
            "reserved",
            "out_of_service",
        ):
            raise ValidationError(
                "Invalid parking spot status."
            )

        if not self.spot_number:
            raise ValidationError(
                "Spot number cannot be empty."
            )

    # ---------- Business Logic ----------

    def occupy(self):

        if self.status != "available":
            raise ParkingSpotUnavailableError(
                f"Parking spot {self.spot_number} is not available."
            )

        self.status = "occupied"

    def release(self):

        if self.status != "occupied":
            raise ValidationError(
                f"Parking spot {self.spot_number} is not occupied."
            )

        self.status = "available"

    def reserve(self):

        if self.status != "available":
            raise ValidationError(
                "Only available spots can be reserved."
            )

        self.status = "reserved"

    def set_out_of_service(self):
        self.status = "out_of_service"

    def is_available(self) -> bool:
        return self.status == "available"