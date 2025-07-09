import os

from .database import DatabaseManager
from .api import MarketplaceAPI

if __name__ == "__main__":
    database_url = os.environ["DATABASE_URL"]
    database = DatabaseManager(database_url)
    api = MarketplaceAPI(database)
    api.app.run(debug=True)
