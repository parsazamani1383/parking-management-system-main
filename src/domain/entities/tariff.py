from dataclasses import dataclass
from datetime import datetime
from src.domain.exceptions import ValidationError


@dataclass
class Tariff:
    id: int | None
    vehicle_type: str  # 'car' or 'motorcycle'
    base_rate: float  # ورودی اولیه (ساعت اول)
    hourly_rate: float  # نرخ ساعتی بعد از ساعت اول
    daily_rate: float  # سقف قیمت روزانه
    is_active: bool
    created_at: datetime

    def __post_init__(self):
        if self.vehicle_type not in ("car", "motorcycle"):
            raise ValidationError("Invalid vehicle type for tariff.")

        if any(rate < 0 for rate in (self.base_rate, self.hourly_rate, self.daily_rate)):
            raise ValidationError("Tariff rates cannot be negative.")

    def deactivate(self):
        self.is_active = False
