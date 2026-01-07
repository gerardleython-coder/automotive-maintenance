"""Tests for Maintenance Strategy Pattern following TDD approach."""
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy
from src.domain.entities.maintenance_alert import AlertType


class TestBasicMaintenanceStrategy:
    """Test cases for BasicMaintenanceStrategy - every 10,000 km."""

    def test_should_generate_alert_at_10000_km(self) -> None:
        """
        Given: BasicMaintenanceStrategy for 10,000 km intervals
        When: Checking if alert should be generated at 10,000 km
        Then: Should return True
        """
        # Arrange
        from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
        strategy = BasicMaintenanceStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=5000, new_mileage=10000)

        # Assert
        assert result is True

    def test_should_not_generate_alert_before_threshold(self) -> None:
        """
        Given: BasicMaintenanceStrategy for 10,000 km intervals
        When: Checking if alert should be generated at 8,000 km
        Then: Should return False
        """
        # Arrange
        from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
        strategy = BasicMaintenanceStrategy()

        # Act
        result = strategy.should_generate_alert(old_mileage=5000, new_mileage=8000)

        # Assert
        assert result is False

    def test_get_alert_type_returns_basic(self) -> None:
        """
        Given: BasicMaintenanceStrategy
        When: Getting alert type
        Then: Should return BASIC_MAINTENANCE
        """
        # Arrange
        from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
        strategy = BasicMaintenanceStrategy()

        # Act
        alert_type = strategy.get_alert_type()

        # Assert
        assert alert_type == AlertType.BASIC_MAINTENANCE
