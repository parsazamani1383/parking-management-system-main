from datetime import datetime

from src.application.interfaces.user_repo import UserRepository


class UpdateUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(
        self,
        user_id: int,
        full_name: str,
        username: str,
        password: str,
        role: str,
        is_active: bool,
    ):

        user = self.user_repo.get_by_id(user_id)

        if user is None:
            raise Exception("کاربر پیدا نشد.")

        # جلوگیری از تکراری بودن نام کاربری
        existing = self.user_repo.get_by_username(username)

        if existing and existing.id != user.id:
            raise Exception("این نام کاربری قبلاً ثبت شده است.")

        user.full_name = full_name
        user.username = username

        if password:
            user.password_hash = password

        user.role = role
        user.is_active = is_active
        user.updated_at = datetime.now()

        self.user_repo.update(user)