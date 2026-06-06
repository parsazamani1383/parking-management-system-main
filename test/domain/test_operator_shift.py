from datetime import datetime, timedelta
import pytest

from src.domain.entities.operator_shift import OperatorShift
from src.domain.exceptions import ValidationError


def create_shift():
    return OperatorShift(
        id=1,
        user_id=10,
        start_time=datetime.now()
    )


# ---------- Creation ----------

def test_valid_shift_creation():
    shift = create_shift()

    assert shift.user_id == 10
    assert shift.start_time is not None
    assert shift.end_time is None
    assert shift.is_active is True


def test_shift_without_start_time_should_fail():
    with pytest.raises(ValidationError):
        OperatorShift(
            id=1,
            user_id=10,
            start_time=None
        )


# ---------- Closing Shift ----------

def test_close_shift_successfully():
    start = datetime.now()
    shift = OperatorShift(id=1, user_id=10, start_time=start)

    end = start + timedelta(hours=8)
    shift.close(end)

    assert shift.end_time == end
    assert shift.is_active is False


def test_close_shift_with_invalid_time_should_fail():
    start = datetime.now()
    shift = OperatorShift(id=1, user_id=10, start_time=start)

    with pytest.raises(ValidationError):
        shift.close(start)


def test_close_shift_before_start_should_fail():
    start = datetime.now()
    shift = OperatorShift(id=1, user_id=10, start_time=start)

    with pytest.raises(ValidationError):
        shift.close(start - timedelta(minutes=10))


def test_close_already_closed_shift_should_fail():
    start = datetime.now()
    shift = OperatorShift(id=1, user_id=10, start_time=start)

    end = start + timedelta(hours=5)
    shift.close(end)

    with pytest.raises(ValidationError):
        shift.close(end + timedelta(hours=1))
