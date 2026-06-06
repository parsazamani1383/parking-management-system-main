import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.infrastructure.db.connection import DatabaseConnection
from src.infrastructure.repositories.vehicle_repo_sqlite import SQLiteVehicleRepository
from src.infrastructure.repositories.parking_spot_repo_sqlite import SQLiteParkingSpotRepository
from src.infrastructure.repositories.parking_session_repo_sqlite import SQLiteParkingSessionRepository
from src.application.use_cases.register_entry import RegisterEntry

def main():
    print("=== Parking Management System CLI ===")

    db_conn = DatabaseConnection()
    conn = db_conn.get_connection()

    vehicle_repo = SQLiteVehicleRepository(conn)
    spot_repo = SQLiteParkingSpotRepository(conn)
    session_repo = SQLiteParkingSessionRepository(conn)

    register_entry = RegisterEntry(vehicle_repo, spot_repo, session_repo)

    plate = input("Enter vehicle plate number: ")
    operator_id = int(input("Enter operator ID: "))
    parking_id = int(input("Enter parking ID: "))

    try:
        session = register_entry.execute(plate, operator_id, parking_id)
        print(f"\n Vehicle registered successfully!")
        print(f"   Session ID: {session.id}")
        print(f"   Spot ID: {session.parking_spot_id}")
        print(f"   Entry Time: {session.entry_time}")
    except Exception as e:
        print(f"\n Error: {e}")

if __name__ == "__main__":
    main()