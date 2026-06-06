from src.config.settings import DATABASE_PATH
from src.infrastructure.db.connection import DatabaseConnection

db = DatabaseConnection(str(DATABASE_PATH))

conn = db.get_connection()

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

for table in tables:
    print(table["name"])

conn.close()