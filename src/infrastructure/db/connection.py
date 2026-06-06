import sqlite3
from pathlib import Path


class DatabaseConnection:
    def __init__(self, db_path: str):
        self._db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._db_path)

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        return connection