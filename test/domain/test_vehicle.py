from datetime import datetime
import pytest

from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions import ValidationError


def create_vehicle(vehicle_type="car"):
    return Vehicle(
        id=1,
        plate_number="12A34567",
        vehicle_type=vehicle_type,
        color="Black",
        brand="Toyota",
        model="Corolla",
        owner_name="Ali",
        owner_phone="09120000000",
        created_at=datetime.now(),
    )


# ---------- Creation Tests ----------

def test_valid_vehicle_creation():
    vehicle = create_vehicle()

    assert vehicle.plate_number == "12A34567"
    assert vehicle.vehicle_type == "car"
    assert vehicle.is_car() is True
    assert vehicle.is_motorcycle() is False


def test_empty_plate_number_should_fail():
    with pytest.raises(ValidationError):
        Vehicle(
            id=1,
            plate_number="",
            vehicle_type="car",
            color=None,
            brand=None,
            model=None,
            owner_name=None,
            owner_phone=None,
            created_at=datetime.now(),
        )


def test_invalid_vehicle_type_should_fail():
    with pytest.raises(ValidationError):
        create_vehicle(vehicle_type="truck")


# ---------- Type Checks ----------

def test_is_motorcycle():
    vehicle = create_vehicle(vehicle_type="motorcycle")

    assert vehicle.is_motorcycle() is True
    assert vehicle.is_car() is False


# ---------- Owner Update ----------

def test_update_owner_successfully():
    vehicle = create_vehicle()
    old_updated_at = vehicle.updated_at

    vehicle.update_owner("Reza", "09129999999")

    assert vehicle.owner_name == "Reza"
    assert vehicle.owner_phone == "09129999999"
    assert vehicle.updated_at is not None
    assert vehicle.updated_at != old_updated_at


def test_update_owner_with_empty_name_should_fail():
    vehicle = create_vehicle()

    with pytest.raises(ValidationError):
        vehicle.update_owner("", "09120000000")
