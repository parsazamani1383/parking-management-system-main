from datetime import datetime

from src.application.interfaces.vehicle_repo import VehicleRepository
from src.domain.entities.vehicle import Vehicle
from src.infrastructure.db.connection import DatabaseConnection


class VehicleRepositorySQLite(VehicleRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(self, row) -> Vehicle:
        return Vehicle(
            id=row["id"],
            plate_number=row["plate_number"],
            vehicle_type=row["vehicle_type"],
            color=row["color"],
            brand=row["brand"],
            model=row["model"],
            owner_name=row["owner_name"],
            owner_phone=row["owner_phone"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=(
                datetime.fromisoformat(row["updated_at"])
                if row["updated_at"]
                else None
            ),
        )

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM vehicle
                WHERE id = ?
                """,
                (vehicle_id,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_by_plate(
        self,
        plate_number: str
    ) -> Vehicle | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM vehicle
                WHERE plate_number = ?
                """,
                (plate_number,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_all(self) -> list[Vehicle]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM vehicle
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

    def save(self, vehicle: Vehicle) -> Vehicle:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO vehicle
                (
                    plate_number,
                    vehicle_type,
                    color,
                    brand,
                    model,
                    owner_name,
                    owner_phone,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    vehicle.plate_number,
                    vehicle.vehicle_type,
                    vehicle.color,
                    vehicle.brand,
                    vehicle.model,
                    vehicle.owner_name,
                    vehicle.owner_phone,
                    vehicle.created_at.isoformat(),
                    (
                        vehicle.updated_at.isoformat()
                        if vehicle.updated_at
                        else None
                    ),
                ),
            )

            conn.commit()

            vehicle.id = cursor.lastrowid

            return vehicle

        finally:
            conn.close()

    def update(self, vehicle: Vehicle) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE vehicle
                SET
                    plate_number = ?,
                    vehicle_type = ?,
                    color = ?,
                    brand = ?,
                    model = ?,
                    owner_name = ?,
                    owner_phone = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    vehicle.plate_number,
                    vehicle.vehicle_type,
                    vehicle.color,
                    vehicle.brand,
                    vehicle.model,
                    vehicle.owner_name,
                    vehicle.owner_phone,
                    (
                        vehicle.updated_at.isoformat()
                        if vehicle.updated_at
                        else None
                    ),
                    vehicle.id,
                ),
            )

            conn.commit()

        finally:
            conn.close()