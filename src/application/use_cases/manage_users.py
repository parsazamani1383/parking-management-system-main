from datetime import datetime

from src.domain.entities.user import User

from src.application.interfaces.user_repo import (
    UserRepository,
)


class ManageUsersUseCase:

    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self._user_repo = user_repo

    def list_users(self):

        return self._user_repo.list_all()

    def add_user(
        self,
        full_name: str,
        username: str,
        password_hash: str,
        role: str,
    ):

        user = User(
            id=None,
            full_name=full_name,
            username=username,
            password_hash=password_hash,
            role=role,
            is_active=True,
            created_at=datetime.now(),
        )

        return self._user_repo.save(
            user
        )

    def delete_user(
        self,
        user_id: int,
    ):

        self._user_repo.delete(
            user_id
        )