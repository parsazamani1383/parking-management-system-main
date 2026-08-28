from datetime import datetime
from math import ceil

from src.domain.entities.tariff import Tariff


class FeeCalculator:

    def calculate(
        self,
        entry_time: datetime,
        exit_time: datetime,
        tariff: Tariff,
    ) -> float:

        duration_hours = (
            exit_time - entry_time
        ).total_seconds() / 3600

        duration_hours = max(
            1,
            ceil(duration_hours)
        )

        fee = tariff.base_rate

        if duration_hours > 1:
            fee += (
                duration_hours - 1
            ) * tariff.hourly_rate

        if (
            tariff.daily_rate > 0
            and fee > tariff.daily_rate
        ):
            fee = tariff.daily_rate

        return float(fee)