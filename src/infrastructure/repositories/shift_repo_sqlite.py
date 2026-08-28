from datetime import datetime

from src.application.interfaces.shift_repo import ShiftRepository
from src.domain.entities.operator_shift import OperatorShift
from src.infrastructure.db.connection import DatabaseConnection


class ShiftRepositorySQLite(ShiftRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(
        self,
        row
    ) -> OperatorShift:

        return OperatorShift(
            id=row["id"],
            user_id=row["user_id"],
            start_time=datetime.fromisoformat(
                row["start_time"]
            ),
            end_time=(
                datetime.fromisoformat(
                    row["end_time"]
                )
                if row["end_time"]
                else None
            ),
        )

    def get_active_shift(
        self,
        user_id: int
    ) -> OperatorShift | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM operator_shift
                WHERE user_id = ?
                  AND shift_status = 'open'
                ORDER BY start_time DESC
                LIMIT 1
                """,
                (user_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def save(
        self,
        shift: OperatorShift
    ) -> OperatorShift:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO operator_shift
                (
                    user_id,
                    parking_id,
                    start_time,
                    end_time,
                    shift_status
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    shift.user_id,
                    1,
                    shift.start_time.isoformat(),
                    (
                        shift.end_time.isoformat()
                        if shift.end_time
                        else None
                    ),
                    (
                        "closed"
                        if shift.end_time
                        else "open"
                    ),
                )
            )

            conn.commit()

            shift.id = cursor.lastrowid

            return shift

        finally:
            conn.close()

    def update(
        self,
        shift: OperatorShift
    ) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE operator_shift
                SET
                    end_time = ?,
                    shift_status = ?
                WHERE id = ?
                """,
                (
                    (
                        shift.end_time.isoformat()
                        if shift.end_time
                        else None
                    ),
                    (
                        "closed"
                        if shift.end_time
                        else "open"
                    ),
                    shift.id,
                )
            )

            conn.commit()

        finally:
            conn.close()