from src.config.settings import DATABASE_PATH
from src.infrastructure.db.connection import DatabaseConnection
from src.infrastructure.repositories.spot_repo_sqlite import (
    SpotRepositorySQLite,
)

db = DatabaseConnection(str(DATABASE_PATH))

repo = SpotRepositorySQLite(db)

spot = repo.get_available_spot("car")

print(spot)

spot.occupy()

repo.update(spot)

updated = repo.get_by_id(spot.id)

print(updated.status)