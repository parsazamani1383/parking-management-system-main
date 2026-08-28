from datetime import datetime

from src.application.interfaces.tariff_repo import TariffRepository
from src.domain.entities.tariff import Tariff
from src.infrastructure.db.connection import DatabaseConnection


class TariffRepositorySQLite(TariffRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(
        self,
        row
    ) -> Tariff:

        return Tariff(
            id=row["id"],
            vehicle_type=row["vehicle_type"],
            base_rate=row["base_amount"],
            hourly_rate=row["hourly_amount"] or 0,
            daily_rate=row["daily_amount"] or 0,
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(
                row["effective_from"]
            ),
        )

    def get_active_tariff(
        self,
        vehicle_type: str
    ) -> Tariff | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM tariff
                WHERE vehicle_type = ?
                  AND is_active = 1
                ORDER BY id
                LIMIT 1
                """,
                (vehicle_type,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_by_id(
        self,
        tariff_id: int
    ) -> Tariff | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM tariff
                WHERE id = ?
                """,
                (tariff_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def save(
        self,
        tariff: Tariff
    ) -> Tariff:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO tariff
                (
                    vehicle_type,
                    tariff_type,
                    base_amount,
                    hourly_amount,
                    daily_amount,
                    fixed_amount,
                    is_active,
                    effective_from
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tariff.vehicle_type,
                    "hourly",
                    tariff.base_rate,
                    tariff.hourly_rate,
                    tariff.daily_rate,
                    None,
                    int(tariff.is_active),
                    tariff.created_at.isoformat(),
                )
            )

            conn.commit()

            tariff.id = cursor.lastrowid

            return tariff

        finally:
            conn.close()

    def update(
        self,
        tariff: Tariff
    ) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE tariff
                SET
                    vehicle_type = ?,
                    base_amount = ?,
                    hourly_amount = ?,
                    daily_amount = ?,
                    is_active = ?
                WHERE id = ?
                """,
                (
                    tariff.vehicle_type,
                    tariff.base_rate,
                    tariff.hourly_rate,
                    tariff.daily_rate,
                    int(tariff.is_active),
                    tariff.id,
                )
            )

            conn.commit()

        finally:
            conn.close()