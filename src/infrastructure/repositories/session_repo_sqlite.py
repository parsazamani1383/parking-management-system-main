from datetime import datetime
from datetime import datetime, timedelta
from src.application.interfaces.session_repo import SessionRepository
from src.domain.entities.parking_session import ParkingSession
from src.infrastructure.db.connection import DatabaseConnection


class SessionRepositorySQLite(SessionRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(
        self,
        row
    ) -> ParkingSession:

        return ParkingSession(
            id=row["id"],
            vehicle_id=row["vehicle_id"],
            spot_id=row["parking_spot_id"],
            shift_id=row["opened_by_user_id"],
            entry_time=datetime.fromisoformat(
                row["entry_time"]
            ),
            exit_time=(
                datetime.fromisoformat(
                    row["exit_time"]
                )
                if row["exit_time"]
                else None
            ),
            total_fee=row["calculated_amount"],
        )

    def get_by_id(
        self,
        session_id: int
    ) -> ParkingSession | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_session
                WHERE id = ?
                """,
                (session_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_active_by_vehicle(
        self,
        vehicle_id: int
    ) -> ParkingSession | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_session
                WHERE vehicle_id = ?
                  AND session_status = 'active'
                LIMIT 1
                """,
                (vehicle_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_all(
            self
    ) -> list[ParkingSession]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_session
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

    def get_active_sessions(
        self
    ) -> list[ParkingSession]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM parking_session
                WHERE session_status = 'active'
                ORDER BY entry_time
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
        session: ParkingSession
    ) -> ParkingSession:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO parking_session
                (
                    parking_id,
                    vehicle_id,
                    parking_spot_id,
                    opened_by_user_id,
                    entry_time,
                    session_status,
                    calculated_amount,
                    paid_amount
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    1,
                    session.vehicle_id,
                    session.spot_id,
                    session.shift_id,
                    session.entry_time.isoformat(),
                    "active",
                    0,
                    0,
                )
            )

            conn.commit()

            session.id = cursor.lastrowid

            return session

        finally:
            conn.close()

    def update(
        self,
        session: ParkingSession
    ) -> None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            status = (
                "completed"
                if session.exit_time
                else "active"
            )

            cursor.execute(
                """
                UPDATE parking_session
                SET
                    parking_spot_id = ?,
                    exit_time = ?,
                    calculated_amount = ?,
                    session_status = ?
                WHERE id = ?
                """,
                (
                    session.spot_id,
                    (
                        session.exit_time.isoformat()
                        if session.exit_time
                        else None
                    ),
                    session.total_fee or 0,
                    status,
                    session.id,
                )
            )

            conn.commit()

        finally:
            conn.close()

    def get_recent_sessions(
            self,
            limit: int = 10
    ) -> list[dict]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT ps.id,
                       v.plate_number,
                       v.vehicle_type,
                       s.spot_number,
                       ps.entry_time,
                       ps.exit_time,
                       ps.session_status
                FROM parking_session ps
                         JOIN vehicle v
                              ON v.id = ps.vehicle_id
                         LEFT JOIN parking_spot s
                                   ON s.id = ps.parking_spot_id
                ORDER BY ps.id DESC LIMIT ?
                """,
                (limit,)
            )

            rows = cursor.fetchall()

            return [
                {
                    "id": row["id"],
                    "plate_number": row["plate_number"],
                    "vehicle_type": row["vehicle_type"],
                    "spot_number": row["spot_number"],
                    "entry_time": row["entry_time"],
                    "exit_time": row["exit_time"],
                    "session_status": row["session_status"],
                }
                for row in rows
            ]

        finally:
            conn.close()

    def search_active_vehicles(
            self,
            plate_filter: str = "",
    ) -> list[dict]:

        conn = self._db.get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT ps.id,
                       ps.entry_time,
                       ps.parking_spot_id,
                       v.id as vehicle_id,
                       v.plate_number,
                       v.vehicle_type,
                       s.spot_number
                FROM parking_session ps
                         JOIN vehicle v
                              ON v.id = ps.vehicle_id
                         LEFT JOIN parking_spot s
                                   ON s.id = ps.parking_spot_id
                WHERE ps.session_status = 'active'
                  AND v.plate_number LIKE ?
                ORDER BY ps.entry_time
                """,
                (
                    f"%{plate_filter}%",
                ),
            )

            rows = cursor.fetchall()

            return [
                {
                    "session_id": row["id"],
                    "vehicle_id": row["vehicle_id"],
                    "plate_number": row["plate_number"],
                    "vehicle_type": row["vehicle_type"],
                    "entry_time": row["entry_time"],
                    "spot_number": row["spot_number"],
                }
                for row in rows
            ]

        finally:
            conn.close()

    def get_active_session_info(
            self,
            session_id: int,
    ):

        conn = self._db.get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    ps.id,
                    v.plate_number,
                    v.vehicle_type,
                    ps.entry_time,
                    s.spot_number
                FROM parking_session ps
                JOIN vehicle v
                    ON v.id = ps.vehicle_id
                LEFT JOIN parking_spot s
                    ON s.id = ps.parking_spot_id
                WHERE ps.id = ?
                """,
                (session_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return dict(row)

        finally:

            conn.close()

    def get_daily_revenue(
            self,
            days: int,
    ) -> list[dict]:

        conn = self._db.get_connection()

        try:

            cursor = conn.cursor()

            start_date = (
                    datetime.now() -
                    timedelta(days=days - 1)
            ).date().isoformat()

            cursor.execute(
                """
                SELECT
                    DATE (exit_time) AS report_date, COUNT (*) AS total_sessions, SUM (calculated_amount) AS total_revenue
                FROM parking_session
                WHERE
                    session_status='completed'
                  AND DATE (exit_time) >= ?
                GROUP BY DATE (exit_time)
                ORDER BY DATE (exit_time) DESC
                """,
                (start_date,)
            )

            rows = cursor.fetchall()

            return [
                {
                    "date": row["report_date"],
                    "sessions": row["total_sessions"],
                    "revenue": row["total_revenue"] or 0,
                }
                for row in rows
            ]

        finally:

            conn.close()