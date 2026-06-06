from src.infrastructure.db.connection import DatabaseConnection
from src.domain.entities.receipt import Receipt
from datetime import datetime


class ReceiptRepoSqlite:

    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def create(self, receipt: Receipt):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO receipt (
                parking_session_id,
                receipt_number,
                issued_by_user_id,
                issued_at,
                amount,
                payment_method,
                payment_status,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            receipt.parking_session_id,
            receipt.receipt_number,
            receipt.issued_by_user_id,
            receipt.issued_at.isoformat(),
            receipt.amount,
            receipt.payment_method,
            receipt.payment_status,
            receipt.description
        ))

        self.conn.commit()
        receipt.id = cursor.lastrowid
        return receipt

    def get_by_session(self, session_id: int):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM receipt
            WHERE parking_session_id = ?
        """, (session_id,))

        row = cursor.fetchone()

        if row:
            data = dict(row)
            data["issued_at"] = datetime.fromisoformat(data["issued_at"])
            return Receipt(**data)

        return None

    def get_receipts_in_range(self, start_date, end_date):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM receipt
            WHERE issued_at BETWEEN ? AND ?
            AND payment_status = 'paid'
        """, (start_date.isoformat(), end_date.isoformat()))

        rows = cursor.fetchall()

        receipts = []

        for row in rows:
            data = dict(row)
            data["issued_at"] = datetime.fromisoformat(data["issued_at"])
            receipts.append(Receipt(**data))

        return receipts
