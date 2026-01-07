"""Tests for InMemoryAlertRepository following TDD approach."""
from datetime import datetime

from src.domain.entities.maintenance_alert import AlertType, MaintenanceAlert
from src.infrastructure.repositories.in_memory_alert_repository import InMemoryAlertRepository


class TestInMemoryAlertRepository:
    """Test cases for InMemoryAlertRepository."""

    def test_save_and_retrieve_alerts(self) -> None:
        """
        Given: An empty repository
        When: Saving multiple alerts
        Then: Should store all alerts correctly
        """
        # Arrange
        repository = InMemoryAlertRepository()
        alert1 = MaintenanceAlert(
            id="A-001",
            vehicle_id="V-123",
            alert_type=AlertType.BASIC_MAINTENANCE,
            mileage=10000,
            timestamp=datetime(2026, 1, 6, 10, 0, 0)
        )
        alert2 = MaintenanceAlert(
            id="A-002",
            vehicle_id="V-123",
            alert_type=AlertType.MAJOR_MAINTENANCE,
            mileage=50000,
            timestamp=datetime(2026, 1, 6, 11, 0, 0)
        )

        # Act
        repository.save(alert1)
        repository.save(alert2)

        # Assert
        assert len(repository.get_all()) == 2
        assert alert1 in repository.get_all()
        assert alert2 in repository.get_all()

    def test_get_all_returns_empty_list_initially(self) -> None:
        """
        Given: A new repository
        When: Getting all alerts
        Then: Should return empty list
        """
        # Arrange
        repository = InMemoryAlertRepository()

        # Act
        alerts = repository.get_all()

        # Assert
        assert alerts == []
