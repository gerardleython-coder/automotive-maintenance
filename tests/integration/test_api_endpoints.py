"""Integration tests for FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.web.main import app
from src.infrastructure.repositories.in_memory_vehicle_repository import InMemoryVehicleRepository
from src.infrastructure.repositories.in_memory_alert_repository import InMemoryAlertRepository
from src.domain.entities.vehicle import Vehicle


class TestVehicleEndpoints:
    """Integration tests for vehicle endpoints."""

    def test_update_vehicle_mileage_successfully(self) -> None:
        """
        Given: A vehicle exists with 5,000 km
        When: PUT /vehicles/{id}/mileage with 8,000 km
        Then: Should return 200 OK and update mileage
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.put(
            "/vehicles/V-123/mileage",
            json={"new_mileage": 8000}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert data["current_mileage"] == 8000

    def test_update_vehicle_mileage_with_invalid_value_returns_400(self) -> None:
        """
        Given: A vehicle exists with 5,000 km
        When: PUT /vehicles/{id}/mileage with 4,000 km (invalid)
        Then: Should return 400 Bad Request
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.put(
            "/vehicles/V-123/mileage",
            json={"new_mileage": 4000}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_update_vehicle_mileage_not_found_returns_404(self) -> None:
        """
        Given: A vehicle does not exist
        When: PUT /vehicles/{id}/mileage
        Then: Should return 404 Not Found
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.put(
            "/vehicles/V-999/mileage",
            json={"new_mileage": 10000}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_get_vehicle_by_id_successfully(self) -> None:
        """
        Given: A vehicle exists
        When: GET /vehicles/{id}
        Then: Should return 200 OK with vehicle data
        """
        # Arrange
        client = TestClient(app)
        
        # Act
        response = client.get("/vehicles/V-123")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "V-123"
        assert "current_mileage" in data

    def test_get_alerts_for_vehicle(self) -> None:
        """
        Given: Alerts exist for a vehicle
        When: GET /vehicles/{id}/alerts
        Then: Should return list of alerts
        """
        # Arrange
        client = TestClient(app)
        
        # First trigger an alert by updating mileage
        client.put("/vehicles/V-123/mileage", json={"new_mileage": 10001})
        
        # Act
        response = client.get("/vehicles/V-123/alerts")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
