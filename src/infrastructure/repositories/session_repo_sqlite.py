from src.infrastructure.db.connection import DatabaseConnection
from src.domain.entities.parking_session import ParkingSession
from datetime import datetime


class SessionRepoSqlite:

    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def save(self, session: ParkingSession):
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO parking_session (
                parking_id,
                vehicle_id,
                parking_spot_id,
                opened_by_user_id,
                entry_time,
                session_status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session.parking_id,
            session.vehicle_id,
            session.parking_spot_id,
            session.opened_by_user_id,
            session.entry_time.isoformat(),
            session.session_status
        ))

        self.conn.commit()
        session.id = cursor.lastrowid
        return session

    def get_active_session_by_plate(self, plate_number):
        cursor = self.conn.cursor()

        cursor.execute("""
                       SELECT ps.*
                       FROM parking_session ps
                                JOIN vehicle v ON ps.vehicle_id = v.id
                       WHERE v.plate_number = ?
                         AND ps.session_status = 'active'
                       """, (plate_number,))

        row = cursor.fetchone()

        if row:
            from datetime import datetime
            data = dict(row)
            data["entry_time"] = datetime.fromisoformat(data["entry_time"])
            return ParkingSession(**data)

        return None

    def update(self, session: ParkingSession):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE parking_session
            SET
                exit_time = ?,
                session_status = ?,
                calculated_amount = ?,
                paid_amount = ?
            WHERE id = ?
        """, (
            session.exit_time.isoformat(),
            session.session_status,
            session.calculated_amount,
            session.paid_amount,
            session.id
        ))

        self.conn.commit()
