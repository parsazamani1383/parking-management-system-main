from datetime import datetime

from src.application.interfaces.parking_repo import (
    ParkingRepository,
)
from src.domain.entities.parking import Parking
from src.infrastructure.db.connection import DatabaseConnection


class ParkingRepositorySQLite(
    ParkingRepository
):

    def __init__(
        self,
        db: DatabaseConnection
    ):
        self._db = db

    def _row_to_entity(
        self,
        row
    ) -> Parking:

        return Parking(
            id=row["id"],
            name=row["name"],
            code=row["code"],
            status=row["status"],
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=(
                datetime.fromisoformat(
                    row["updated_at"]
                )
                if row["updated_at"]
                else None
            ),
        )

    def get_by_id(
        self,
        parking_id: int
    ) -> Parking | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking
                WHERE id = ?
                """,
                (parking_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_current(
        self
    ) -> Parking | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking
                ORDER BY id
                LIMIT 1
                """
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()