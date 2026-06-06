from datetime import datetime, timedelta
import pytest

from src.domain.entities.parking_spot import ParkingSpot
from src.domain.exceptions import ValidationError, ParkingSpotUnavailableError


def create_spot(is_occupied=False):
    return ParkingSpot(
        id=1,
        spot_number="A1",
        vehicle_type="car",
        is_occupied=is_occupied,
        created_at=datetime.now(),
    )


# ---------- Creation Tests ----------

def test_valid_spot_creation():
    spot = create_spot()

    assert spot.spot_number == "A1"
    assert spot.vehicle_type == "car"
    assert spot.is_occupied is False
    assert spot.is_available() is True


def test_invalid_vehicle_type_should_fail():
    with pytest.raises(ValidationError):
        ParkingSpot(
            id=1,
            spot_number="A1",
            vehicle_type="truck",
            is_occupied=False,
            created_at=datetime.now(),
        )


def test_empty_spot_number_should_fail():
    with pytest.raises(ValidationError):
        ParkingSpot(
            id=1,
            spot_number="",
            vehicle_type="car",
            is_occupied=False,
            created_at=datetime.now(),
        )


# ---------- Business Logic Tests ----------

def test_occupy_successfully():
    spot = create_spot()

    spot.occupy()

    assert spot.is_occupied is True
    assert spot.is_available() is False
    assert spot.updated_at is not None


def test_occupy_already_occupied_should_fail():
    spot = create_spot(is_occupied=True)

    with pytest.raises(ParkingSpotUnavailableError):
        spot.occupy()


def test_release_successfully():
    spot = create_spot(is_occupied=True)

    spot.release()

    assert spot.is_occupied is False
    assert spot.is_available() is True
    assert spot.updated_at is not None


def test_release_when_not_occupied_should_fail():
    spot = create_spot(is_occupied=False)

    with pytest.raises(ValidationError):
        spot.release()
