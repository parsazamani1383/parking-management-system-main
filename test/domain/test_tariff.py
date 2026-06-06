from datetime import datetime
import pytest

from src.domain.entities.tariff import Tariff
from src.domain.exceptions import ValidationError


def create_tariff(vehicle_type="car"):
    return Tariff(
        id=1,
        vehicle_type=vehicle_type,
        base_rate=10.0,
        hourly_rate=5.0,
        daily_rate=50.0,
        is_active=True,
        created_at=datetime.now(),
    )


# ---------- Creation ----------

def test_valid_tariff_creation():
    tariff = create_tariff()

    assert tariff.vehicle_type == "car"
    assert tariff.base_rate == 10.0
    assert tariff.hourly_rate == 5.0
    assert tariff.daily_rate == 50.0
    assert tariff.is_active is True


def test_invalid_vehicle_type_should_fail():
    with pytest.raises(ValidationError):
        create_tariff(vehicle_type="truck")


# ---------- Rate Validation ----------

def test_negative_base_rate_should_fail():
    with pytest.raises(ValidationError):
        Tariff(
            id=1,
            vehicle_type="car",
            base_rate=-1,
            hourly_rate=5,
            daily_rate=50,
            is_active=True,
            created_at=datetime.now(),
        )


def test_negative_hourly_rate_should_fail():
    with pytest.raises(ValidationError):
        Tariff(
            id=1,
            vehicle_type="car",
            base_rate=10,
            hourly_rate=-5,
            daily_rate=50,
            is_active=True,
            created_at=datetime.now(),
        )


def test_negative_daily_rate_should_fail():
    with pytest.raises(ValidationError):
        Tariff(
            id=1,
            vehicle_type="car",
            base_rate=10,
            hourly_rate=5,
            daily_rate=-50,
            is_active=True,
            created_at=datetime.now(),
        )


# ---------- State Change ----------

def test_deactivate_tariff():
    tariff = create_tariff()

    tariff.deactivate()

    assert tariff.is_active is False
