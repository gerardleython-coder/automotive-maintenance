"""Tests for UpdateVehicleMileageUseCase following TDD approach."""
import pytest
from datetime import datetime
from src.application.use_cases.update_vehicle_mileage_use_case import UpdateVehicleMileageUseCase
from src.domain.entities.vehicle import Vehicle
from src.domain.entities.maintenance_alert import MaintenanceAlert, AlertType
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException


class InMemoryVehicleRepository:
    """In-memory repository for testing."""

    def __init__(self):
        self.vehicles = {}

    def get_by_id(self, vehicle_id: str) -> Vehicle:
        """Get vehicle by ID."""
        if vehicle_id not in self.vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        return self.vehicles[vehicle_id]

    def save(self, vehicle: Vehicle) -> None:
        """Save vehicle."""
        self.vehicles[vehicle.id] = vehicle


class MockAlertRepository:
    """Mock alert repository for testing."""

    def __init__(self):
        self.alerts = []

    def save(self, alert: MaintenanceAlert) -> None:
        """Save alert."""
        self.alerts.append(alert)


class TestUpdateVehicleMileageUseCase:
    """Test cases for UpdateVehicleMileageUseCase."""

    def test_update_mileage_successfully(self) -> None:
        """
        Given: A vehicle with 5,000 km
        When: Updating mileage to 8,000 km
        Then: Vehicle mileage should be updated
        And: Vehicle should be persisted
        """
        # Arrange
        vehicle_repo = InMemoryVehicleRepository()
        alert_repo = MockAlertRepository()
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        vehicle_repo.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repo,
            alert_repository=alert_repo
        )

        # Act
        use_case.execute(vehicle_id="V-123", new_mileage=8000)

        # Assert
        updated_vehicle = vehicle_repo.get_by_id("V-123")
        assert updated_vehicle.current_mileage == 8000

    def test_update_mileage_with_invalid_value_raises_exception(self) -> None:
        """
        Given: A vehicle with 5,000 km
        When: Attempting to update with invalid mileage (4,000 km)
        Then: Should raise InvalidMileageException
        """
        # Arrange
        vehicle_repo = InMemoryVehicleRepository()
        alert_repo = MockAlertRepository()
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        vehicle_repo.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repo,
            alert_repository=alert_repo
        )

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            use_case.execute(vehicle_id="V-123", new_mileage=4000)

    def test_update_mileage_crossing_10k_threshold_generates_alert(self) -> None:
        """
        Given: A vehicle with 5,000 km and basic maintenance strategy
        When: Updating mileage to 10,001 km
        Then: Should generate and persist a basic maintenance alert
        """
        # Arrange
        vehicle_repo = InMemoryVehicleRepository()
        alert_repo = MockAlertRepository()
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        vehicle_repo.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repo,
            alert_repository=alert_repo
        )

        # Act
        use_case.execute(vehicle_id="V-123", new_mileage=10001)

        # Assert
        assert len(alert_repo.alerts) == 1
        alert = alert_repo.alerts[0]
        assert alert.vehicle_id == "V-123"
        assert alert.mileage == 10001
        assert alert.alert_type == AlertType.BASIC_MAINTENANCE
