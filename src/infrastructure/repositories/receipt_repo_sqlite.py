from datetime import datetime

from src.application.interfaces.receipt_repo import ReceiptRepository
from src.domain.entities.receipt import Receipt
from src.infrastructure.db.connection import DatabaseConnection


class ReceiptRepositorySQLite(ReceiptRepository):

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def _row_to_entity(
        self,
        row
    ) -> Receipt:

        return Receipt(
            id=row["id"],
            session_id=row["parking_session_id"],
            receipt_number=row["receipt_number"],
            amount=row["amount"],
            payment_method=row["payment_method"],
            issued_at=datetime.fromisoformat(
                row["issued_at"]
            ),
        )

    def get_by_id(
        self,
        receipt_id: int
    ) -> Receipt | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM receipt
                WHERE id = ?
                """,
                (receipt_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_by_session(
        self,
        session_id: int
    ) -> Receipt | None:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM receipt
                WHERE parking_session_id = ?
                """,
                (session_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_entity(row)

        finally:
            conn.close()

    def get_all(
            self
    ) -> list[Receipt]:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM receipt
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
        receipt: Receipt
    ) -> Receipt:

        conn = self._db.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO receipt
                (
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
                """,
                (
                    receipt.session_id,
                    receipt.receipt_number,
                    1,
                    receipt.issued_at.isoformat(),
                    receipt.amount,
                    receipt.payment_method,
                    "paid",
                    None,
                )
            )

            conn.commit()

            receipt.id = cursor.lastrowid

            return receipt

        finally:
            conn.close()