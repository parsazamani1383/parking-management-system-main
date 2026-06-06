from datetime import datetime
from src.application.services.fee_calculator import FeeCalculator


class RegisterExit:

    def __init__(self, session_repo, spot_repo, tariff_repo, receipt_repo):

        self.session_repo = session_repo
        self.spot_repo = spot_repo
        self.tariff_repo = tariff_repo
        self.receipt_repo = receipt_repo


    def execute(self, license_plate: str, payment_method: str = "cash"):

        # 1. پیدا کردن session فعال
        session = self.session_repo.get_active_session_by_plate(license_plate)

        if not session:
            raise Exception(f"No active session found for {license_plate}")

        # 2. زمان خروج
        exit_time = datetime.now()

        # 3. گرفتن تعرفه فعال
        tariff = self.tariff_repo.get_tariff_by_vehicle_type("car")

        if not tariff:
            raise Exception("No active tariff found")

        # 4. محاسبه هزینه
        total_fee = FeeCalculator.calculate_fee(
            session.entry_time,
            exit_time,
            tariff
        )

        # 5. آزاد کردن جای پارک
        self.spot_repo.update_status(session.parking_spot_id, "available")

        # 6. بستن session
        session.exit_time = exit_time
        session.calculated_amount = total_fee
        session.paid_amount = total_fee
        session.session_status = "completed"

        self.session_repo.update(session)

        # 7. صدور رسید
        receipt_number = self.receipt_repo.create(
            session_id=session.id,
            amount=total_fee,
            payment_method=payment_method
        )

        # 8. خروجی
        return {
            "status": "success",
            "license_plate": license_plate,
            "entry_time": session.entry_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": str(exit_time - session.entry_time).split('.')[0],
            "total_fee": total_fee,
            "receipt_number": receipt_number,
            "spot_released": session.parking_spot_id
        }
