from datetime import datetime
import pytest

from src.domain.entities.receipt import Receipt
from src.domain.exceptions import ValidationError


def create_receipt():
    return Receipt(
        id=1,
        session_id=10,
        receipt_number="R-1001",
        amount=25.0,
        payment_method="cash",
        issued_at=datetime.now(),
    )


# ---------- Creation ----------

def test_valid_receipt_creation():
    receipt = create_receipt()

    assert receipt.receipt_number == "R-1001"
    assert receipt.amount == 25.0
    assert receipt.payment_method == "cash"
    assert receipt.session_id == 10


def test_empty_receipt_number_should_fail():
    with pytest.raises(ValidationError):
        Receipt(
            id=1,
            session_id=10,
            receipt_number="",
            amount=20,
            payment_method="cash",
            issued_at=datetime.now(),
        )


def test_negative_amount_should_fail():
    with pytest.raises(ValidationError):
        Receipt(
            id=1,
            session_id=10,
            receipt_number="R-1002",
            amount=-5,
            payment_method="cash",
            issued_at=datetime.now(),
        )


def test_invalid_payment_method_should_fail():
    with pytest.raises(ValidationError):
        Receipt(
            id=1,
            session_id=10,
            receipt_number="R-1003",
            amount=20,
            payment_method="bitcoin",
            issued_at=datetime.now(),
        )


# ---------- Formatting ----------

def test_format_for_print():
    receipt = create_receipt()

    result = receipt.format_for_print()

    assert "R-1001" in result
    assert "25.0" in result
    assert "Receipt:" in result
