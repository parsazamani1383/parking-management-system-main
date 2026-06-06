from datetime import datetime
import pytest

from src.domain.entities.user import User
from src.domain.exceptions import ValidationError


def create_user(role="operator", active=True):
    return User(
        id=1,
        full_name="Ali Ahmadi",
        username="ali",
        password_hash="hashed_password",
        role=role,
        is_active=active,
        created_at=datetime.now(),
    )


# ---------- Creation Tests ----------

def test_valid_user_creation():
    user = create_user()

    assert user.username == "ali"
    assert user.role == "operator"
    assert user.is_operator() is True
    assert user.is_admin() is False
    assert user.is_active is True


def test_invalid_role_should_fail():
    with pytest.raises(ValidationError):
        create_user(role="manager")


def test_empty_username_should_fail():
    with pytest.raises(ValidationError):
        User(
            id=1,
            full_name="Ali",
            username="",
            password_hash="hash",
            role="operator",
            is_active=True,
            created_at=datetime.now(),
        )


# ---------- Role Checks ----------

def test_admin_role_detection():
    user = create_user(role="admin")

    assert user.is_admin() is True
    assert user.is_operator() is False


# ---------- Activation / Deactivation ----------

def test_deactivate_user():
    user = create_user(active=True)

    user.deactivate()

    assert user.is_active is False
    assert user.updated_at is not None


def test_activate_user():
    user = create_user(active=False)

    user.activate()

    assert user.is_active is True
    assert user.updated_at is not None
