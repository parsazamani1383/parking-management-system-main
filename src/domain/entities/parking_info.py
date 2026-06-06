from dataclasses import dataclass
from src.domain.exceptions import ValidationError


@dataclass
class ParkingInfo:
    id: int | None
    name: str
    address: str
    total_capacity: int
    car_capacity: int
    motorcycle_capacity: int

    def __post_init__(self):
        if self.total_capacity <= 0:
            raise ValidationError("Total capacity must be positive.")

        if self.car_capacity < 0 or self.motorcycle_capacity < 0:
            raise ValidationError("Vehicle capacities cannot be negative.")

        if self.car_capacity + self.motorcycle_capacity != self.total_capacity:
            raise ValidationError(
                "Sum of car and motorcycle capacity must equal total capacity."
            )

    # -------- Business Logic --------

    def has_available_space(
        self,
        car_occupied: int,
        motorcycle_occupied: int,
        vehicle_type: str,
    ) -> bool:

        if vehicle_type == "car":
            return car_occupied < self.car_capacity

        if vehicle_type == "motorcycle":
            return motorcycle_occupied < self.motorcycle_capacity

        raise ValidationError("Invalid vehicle type.")
