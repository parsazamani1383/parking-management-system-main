from datetime import datetime
from src.application.interfaces.shift_repo import OperatorShiftRepository
from src.domain.entities.operator_shift import OperatorShift
from src.infrastructure.db.connection import DatabaseConnection

class OperatorShiftRepoSqlite(OperatorShiftRepository):
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def start_shift(self, operator_id: int):
        cursor = self.conn.cursor()
        start_time = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO operator_shift (operator_id, start_time, shift_status)
            VALUES (?, ?, 'open')
        """, (operator_id, start_time))
        self.conn.commit()
        return cursor.lastrowid

    def end_shift(self, shift_id: int):
        cursor = self.conn.cursor()
        end_time = datetime.now().isoformat()
        cursor.execute("""
            UPDATE operator_shift 
            SET end_time = ?, shift_status = 'closed' 
            WHERE id = ?
        """, (end_time, shift_id))
        self.conn.commit()
