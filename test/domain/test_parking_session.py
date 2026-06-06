from datetime import datetime, timedelta
import pytest

from src.domain.entities.parking_session import ParkingSession
from src.domain.exceptions import ValidationError, SessionAlreadyClosedError


def create_session():
    return ParkingSession(
        id=1,
        vehicle_id=1,
        spot_id=5,
        shift_id=2,
        entry_time=datetime.now()
    )


def test_session_creation():
    session = create_session()

    assert session.id == 1
    assert session.exit_time is None
    assert session.total_fee is None
    assert session.is_active is True


def test_close_session_successfully():
    session = create_session()

    exit_time = session.entry_time + timedelta(hours=2)

    session.close(exit_time, 5000)

    assert session.exit_time == exit_time
    assert session.total_fee == 5000
    assert session.is_active is False


def test_close_session_twice_should_fail():
    session = create_session()

    exit_time = session.entry_time + timedelta(hours=1)

    session.close(exit_time, 3000)

    with pytest.raises(SessionAlreadyClosedError):
        session.close(exit_time, 3000)


def test_exit_time_before_entry_should_fail():
    session = create_session()

    invalid_exit = session.entry_time - timedelta(minutes=10)

    with pytest.raises(ValidationError):
        session.close(invalid_exit, 1000)


def test_negative_fee_should_fail():
    session = create_session()

    exit_time = session.entry_time + timedelta(hours=1)

    with pytest.raises(ValidationError):
        session.close(exit_time, -100)
