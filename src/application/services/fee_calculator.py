from datetime import timedelta


class FeeCalculator:

    @staticmethod
    def calculate_fee(entry_time, exit_time, tariff):

        duration = exit_time - entry_time
        total_hours = duration.total_seconds() / 3600

        # اگر کمتر از یک ساعت بود → ساعت اول حساب شود
        if total_hours <= 1:
            return tariff["base_amount"]

        # اگر بیشتر از 24 ساعت
        if total_hours >= 24:
            days = int(total_hours // 24)
            remaining_hours = total_hours % 24

            fee = days * tariff["daily_amount"]

            if remaining_hours > 0:
                if remaining_hours <= 1:
                    fee += tariff["base_amount"]
                else:
                    fee += tariff["base_amount"] + \
                           (int(remaining_hours - 1) * tariff["hourly_amount"])

            return fee

        # بین 1 تا 24 ساعت
        remaining_hours = total_hours - 1

        return (
            tariff["base_amount"] +
            int(remaining_hours) * tariff["hourly_amount"]
        )
