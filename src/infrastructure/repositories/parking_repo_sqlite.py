from src.application.interfaces.parking_repository import ParkingRepository
from src.infrastructure.db.connection import DatabaseConnection

class ParkingRepoSqlite(ParkingRepository):
    def __init__(self):
        self.conn = DatabaseConnection.get_connection()

    def get_info(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM parking_info LIMIT 1")
        return dict(cursor.fetchone())

    def get_current_occupancy(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM parking_spot WHERE status = 'occupied') as occupied_count,
                (SELECT total_capacity FROM parking_info LIMIT 1) as total_capacity
        """)
        return dict(cursor.fetchone())
