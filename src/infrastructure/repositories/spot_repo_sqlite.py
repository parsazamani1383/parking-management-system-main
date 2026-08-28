from src.application.interfaces.spot_repo import SpotRepository
from src.domain.entities.parking_spot import ParkingSpot
from src.infrastructure.db.connection import DatabaseConnection


class SpotRepositorySQLite(SpotRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(
        self,
        row
    ) -> ParkingSpot:

        return ParkingSpot(
            id=row["id"],
            parking_id=row["parking_id"],
            spot_number=row["spot_number"],
            spot_type=row["spot_type"],
            status=row["status"],
            level_label=row["level_label"],
            section_label=row["section_label"],
            is_active=bool(row["is_active"]),
        )

    def get_by_id(
        self,
        spot_id: int
    ) -> ParkingSpot | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_spot
                WHERE id = ?
                """,
                (spot_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_available_spot(
        self,
        spot_type: str
    ) -> ParkingSpot | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_spot
                WHERE spot_type = ?
                  AND status = 'available'
                  AND is_active = 1
                ORDER BY id
                LIMIT 1
                """,
                (spot_type,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_all(self) -> list[ParkingSpot]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_spot
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

    def save(
        self,
        spot: ParkingSpot
    ) -> ParkingSpot:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO parking_spot
                (
                    parking_id,
                    spot_number,
                    spot_type,
                    status,
                    level_label,
                    section_label,
                    is_active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    spot.parking_id,
                    spot.spot_number,
                    spot.spot_type,
                    spot.status,
                    spot.level_label,
                    spot.section_label,
                    int(spot.is_active),
                )
            )

            conn.commit()

            spot.id = cursor.lastrowid

            return spot

        finally:
            conn.close()

    def update(
        self,
        spot: ParkingSpot
    ) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE parking_spot
                SET
                    parking_id = ?,
                    spot_number = ?,
                    spot_type = ?,
                    status = ?,
                    level_label = ?,
                    section_label = ?,
                    is_active = ?
                WHERE id = ?
                """,
                (
                    spot.parking_id,
                    spot.spot_number,
                    spot.spot_type,
                    spot.status,
                    spot.level_label,
                    spot.section_label,
                    int(spot.is_active),
                    spot.id,
                )
            )

            conn.commit()

        finally:
            conn.close()

    def get_by_number(
            self,
            spot_number: str,
    ) -> ParkingSpot | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_spot
                WHERE spot_number = ?
                """,
                (spot_number,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def delete(
            self,
            spot_id: int,
    ) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE
                FROM parking_spot
                WHERE id = ?
                """,
                (spot_id,),
            )

            conn.commit()

        finally:
            conn.close()