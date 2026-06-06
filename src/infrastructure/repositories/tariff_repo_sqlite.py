from src.infrastructure.db.connection import DatabaseConnection


class TariffRepoSqlite:

    def __init__(self):
        self.conn = DatabaseConnection.get_connection()


    def get_tariff_by_vehicle_type(self, vehicle_type):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT *
            FROM tariff
            WHERE vehicle_type = ?
            AND is_active = 1
            ORDER BY effective_from DESC
            LIMIT 1
        """, (vehicle_type,))

        row = cursor.fetchone()

        if row:
            return dict(row)

        return None


    def save(self, tariff):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO tariff (
                vehicle_type,
                tariff_type,
                base_amount,
                hourly_amount,
                daily_amount,
                effective_from,
                is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tariff.vehicle_type,
            tariff.tariff_type,
            tariff.base_amount,
            tariff.hourly_amount,
            tariff.daily_amount,
            tariff.effective_from,
            tariff.is_active
        ))

        self.conn.commit()

        tariff.id = cursor.lastrowid
        return tariff


    def update(self, tariff):

        cursor = self.conn.cursor()

        cursor.execute("""
            UPDATE tariff
            SET
                base_amount = ?,
                hourly_amount = ?,
                daily_amount = ?,
                is_active = ?
            WHERE id = ?
        """, (
            tariff.base_amount,
            tariff.hourly_amount,
            tariff.daily_amount,
            tariff.is_active,
            tariff.id
        ))

        self.conn.commit()
