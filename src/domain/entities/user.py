from dataclasses import dataclass
from datetime import datetime
from src.domain.exceptions import ValidationError


@dataclass
class User:
    id: int | None
    full_name: str
    username: str
    password_hash: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    def __post_init__(self):
        if self.role not in ("owner", "admin", "operator"):
            raise ValidationError("Invalid user role.")

        if not self.username:
            raise ValidationError("Username cannot be empty.")

    # ---- Business Logic ----

    def is_owner(self) -> bool:
        return self.role == "owner"

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_operator(self) -> bool:
        return self.role == "operator"

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now()