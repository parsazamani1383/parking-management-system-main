from datetime import datetime

from src.application.interfaces.user_repo import UserRepository
from src.domain.entities.user import User
from src.domain.exceptions import ValidationError


class CreateUserUseCase:

    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    def execute(
        self,
        full_name: str,
        username: str,
        password: str,
        role: str,
        is_active: bool,
    ) -> User:

        if self.user_repo.get_by_username(username):
            raise ValidationError(
                "نام کاربری قبلاً ثبت شده است."
            )

        user = User(
            id=None,
            full_name=full_name,
            username=username,
            password_hash=password,
            role=role,
            is_active=is_active,
            created_at=datetime.now(),
        )

        return self.user_repo.save(user)