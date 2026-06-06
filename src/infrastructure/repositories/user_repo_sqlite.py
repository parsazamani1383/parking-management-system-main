from datetime import datetime

from src.application.interfaces.user_repo import UserRepository
from src.domain.entities.user import User
from src.infrastructure.db.connection import DatabaseConnection


class UserRepositorySQLite(UserRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(self, row) -> User:
        return User(
            id=row["id"],
            full_name=row["full_name"],
            username=row["username"],
            password_hash=row["password_hash"],
            role=row["role"],
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=(
                datetime.fromisoformat(row["updated_at"])
                if row["updated_at"]
                else None
            ),
        )

    def get_by_id(self, user_id: int) -> User | None:
        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM user
                WHERE id = ?
                """,
                (user_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_by_username(
        self,
        username: str
    ) -> User | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM user
                WHERE username = ?
                """,
                (username,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def list_all(self) -> list[User]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM user
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

            return [
                self._row_to_entity(row)
                for row in rows
            ]

        finally:
            conn.close()
    def save(self, user: User) -> User:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO user
                (
                    full_name,
                    username,
                    password_hash,
                    role,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user.full_name,
                    user.username,
                    user.password_hash,
                    user.role,
                    int(user.is_active),
                    user.created_at.isoformat(),
                    (
                        user.updated_at.isoformat()
                        if user.updated_at
                        else None
                    ),
                ),
            )

            conn.commit()

            user.id = cursor.lastrowid

            return user

        finally:
            conn.close()

    def update(self, user: User) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE user
                SET
                    full_name = ?,
                    username = ?,
                    password_hash = ?,
                    role = ?,
                    is_active = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    user.full_name,
                    user.username,
                    user.password_hash,
                    user.role,
                    int(user.is_active),
                    (
                        user.updated_at.isoformat()
                        if user.updated_at
                        else None
                    ),
                    user.id,
                ),
            )

            conn.commit()

        finally:
            conn.close()

    def delete(self, user_id: int) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM user
                WHERE id = ?
                """,
                (user_id,),
            )

            conn.commit()

        finally:
            conn.close()