from datetime import datetime
from uuid import uuid4

from src.domain.entities.receipt import Receipt
from src.application.services.fee_calculator import (
    FeeCalculator,
)
from src.application.interfaces.vehicle_repo import (
    VehicleRepository,
)

from src.application.interfaces.session_repo import (
    SessionRepository,
)

from src.application.interfaces.spot_repo import (
    SpotRepository,
)

from src.application.interfaces.receipt_repo import (
    ReceiptRepository,
)

from src.application.interfaces.tariff_repo import (
    TariffRepository,
)

from src.domain.exceptions import ValidationError


class RegisterExitUseCase:

    def __init__(
        self,
        vehicle_repo: VehicleRepository,
        session_repo: SessionRepository,
        spot_repo: SpotRepository,
        receipt_repo: ReceiptRepository,
        tariff_repo: TariffRepository,
    ):

        self._vehicle_repo = vehicle_repo
        self._session_repo = session_repo
        self._spot_repo = spot_repo
        self._receipt_repo = receipt_repo
        self._tariff_repo = tariff_repo

        self._calculator = (
            FeeCalculator()
        )

    def execute(
        self,
        plate_number: str,
        payment_method: str,
    ):

        vehicle = (
            self._vehicle_repo
            .get_by_plate(
                plate_number
            )
        )

        if vehicle is None:

            raise ValidationError(
                "خودرو یافت نشد"
            )

        session = (
            self._session_repo
            .get_active_by_vehicle(
                vehicle.id
            )
        )

        if session is None:

            raise ValidationError(
                "خودرو داخل پارکینگ نیست"
            )

        tariff = (
            self._tariff_repo
            .get_active_tariff(
                vehicle.vehicle_type
            )
        )

        if tariff is None:

            raise ValidationError(
                "تعرفه فعال یافت نشد"
            )

        exit_time = datetime.now()

        fee = (
            self._calculator
            .calculate(
                session.entry_time,
                exit_time,
                tariff,
            )
        )

        session.close(
            exit_time,
            fee,
        )

        self._session_repo.update(
            session
        )

        spot = (
            self._spot_repo
            .get_by_id(
                session.spot_id
            )
        )

        if spot:

            spot.release()

            self._spot_repo.update(
                spot
            )

        receipt = Receipt(
            id=None,
            session_id=session.id,
            receipt_number=datetime.now().strftime("%Y%m%d%H%M%S"),
            amount=fee,
            payment_method=payment_method,
            issued_at=datetime.now(),
        )

        receipt = (
            self._receipt_repo
            .save(
                receipt
            )
        )

        return {
            "vehicle": vehicle,
            "session": session,
            "receipt": receipt,
            "fee": fee,
        }