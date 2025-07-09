import pytest
from backend_marketplace.database import DatabaseManager
from backend_marketplace.api import MarketplaceAPI


class TestMarketplaceAPI:
    @pytest.fixture
    def db(self):
        """Create an in-memory database for testing."""
        return DatabaseManager(":memory:")

    @pytest.fixture
    def api(self, db):
        """Create API instance with in-memory database."""
        return MarketplaceAPI(db)

    @pytest.fixture
    def client(self, api):
        """Create Flask test client."""
        return api.app.test_client()

    def test_register_buyer_endpoint(self, client, db):
        """Test the buyers register API endpoint stores data in database."""
        user_data = {"name": "John Doe", "email": "john@example.com"}

        response = client.post("/api/buyers/register", json=user_data)

        assert response.status_code == 201
        assert response.is_json

        # Check API response includes user ID and success message
        data = response.get_json()
        assert "id" in data
        assert data["message"] == "User registered successfully"
        assert isinstance(data["id"], int)

        # Verify data was actually stored in database
        db.cursor.execute(
            "SELECT name, email, role FROM users WHERE id = ?", (data["id"],)
        )
        result = db.cursor.fetchone()

        assert result is not None
        assert result[0] == user_data["name"]
        assert result[1] == user_data["email"]
        assert result[2] == "buyer"

    def test_register_seller_endpoint(self, client, db):
        """Test the sellers register API endpoint stores data in database."""
        user_data = {"name": "Jane Smith", "email": "jane@example.com"}

        response = client.post("/api/sellers/register", json=user_data)

        assert response.status_code == 201
        assert response.is_json

        # Check API response includes user ID and success message
        data = response.get_json()
        assert "id" in data
        assert data["message"] == "User registered successfully"
        assert isinstance(data["id"], int)

        # Verify data was actually stored in database
        db.cursor.execute(
            "SELECT name, email, role FROM users WHERE id = ?", (data["id"],)
        )
        result = db.cursor.fetchone()

        assert result is not None
        assert result[0] == user_data["name"]
        assert result[1] == user_data["email"]
        assert result[2] == "seller"
