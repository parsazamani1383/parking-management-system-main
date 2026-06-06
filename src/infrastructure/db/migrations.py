# src/infrastructure/db/migrations.py

from pathlib import Path
from src.infrastructure.db.connection import DatabaseConnection


class DatabaseInitializer:

    @staticmethod
    def initialize_database():

        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()

        project_root = Path(__file__).resolve().parents[3]
        data_path = project_root / "data"

        schema_file = data_path / "schema.sql"
        seed_file = data_path / "seed.sql"

        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)

        cursor.execute("SELECT COUNT(*) as count FROM parking;")
        result = cursor.fetchone()

        if result["count"] == 0:
            with open(seed_file, "r", encoding="utf-8") as f:
                seed_sql = f.read()
                cursor.executescript(seed_sql)

        conn.commit()
