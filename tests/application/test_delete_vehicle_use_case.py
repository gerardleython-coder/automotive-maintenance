"""Tests for DeleteVehicleUseCase - Application layer."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.application.use_cases.delete_vehicle_use_case import DeleteVehicleUseCase
from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.vehicle_not_found_exception import (
    VehicleNotFoundException,
)
from src.infrastructure.database.models import Base
from src.infrastructure.repositories.sqlite_alert_repository import (
    SqliteAlertRepository,
)
from src.infrastructure.repositories.sqlite_vehicle_repository import (
    SqliteVehicleRepository,
)


@pytest.fixture
def test_db():
    """Create clean persistent SQLite database for each test."""
    engine = create_engine("sqlite:///test_maintenance.db")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)
    session = session_local()

    yield session

    # Cleanup after test
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def vehicle_repository(test_db):
    """Create vehicle repository instance with test database."""
    return SqliteVehicleRepository(test_db)


@pytest.fixture
def alert_repository(test_db):
    """Create alert repository instance with test database."""
    return SqliteAlertRepository(test_db)


class TestDeleteVehicleUseCase:
    """Test suite for DeleteVehicleUseCase."""

    def test_delete_vehicle_successfully(self, vehicle_repository):
        """
        Test deleting an existing vehicle.

        Given a vehicle exists in the system
        When delete use case is executed with the vehicle ID
        Then the vehicle should be removed from the database
        And subsequent queries for the vehicle should raise VehicleNotFoundException
        """
        # Arrange
        vehicle = Vehicle(
            id="V-999", plate="XYZ-999", model="Honda Accord", current_mileage=20000
        )
        vehicle_repository.save(vehicle)

        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act
        use_case.execute(vehicle_id="V-999")

        # Assert
        with pytest.raises(VehicleNotFoundException):
            vehicle_repository.get_by_id("V-999")

    def test_delete_nonexistent_vehicle_raises_exception(self, vehicle_repository):
        """
        Test deleting a vehicle that doesn't exist.

        Given no vehicle exists with the given ID
        When delete use case is executed
        Then VehicleNotFoundException should be raised
        And the error message should indicate vehicle not found
        """
        # Arrange
        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act & Assert
        with pytest.raises(VehicleNotFoundException) as exc_info:
            use_case.execute(vehicle_id="V-NONEXISTENT")

        assert "Vehículo con ID V-NONEXISTENT no encontrado" in str(exc_info.value)

    def test_delete_vehicle_cascades_alerts(
        self, vehicle_repository, alert_repository
    ):
        """
        Test that deleting a vehicle also deletes all associated alerts (cascade).

        Given a vehicle exists with multiple alerts
        When the vehicle is deleted
        Then all alerts associated with that vehicle should also be deleted
        And no orphan alerts should remain in the database
        """
        # Arrange
        vehicle = Vehicle(
            id="V-777", plate="ABC-777", model="Toyota Camry", current_mileage=30000
        )
        vehicle_repository.save(vehicle)

        # Create multiple alerts for the vehicle
        alert1 = MaintenanceAlert(
            vehicle_id="V-777",
            alert_type="BASIC",
            mileage_threshold=10000,
            message="Mantenimiento básico",
        )
        alert2 = MaintenanceAlert(
            vehicle_id="V-777",
            alert_type="MAJOR",
            mileage_threshold=50000,
            message="Mantenimiento mayor",
        )
        alert3 = MaintenanceAlert(
            vehicle_id="V-777",
            alert_type="CRITICAL",
            mileage_threshold=100000,
            message="Mantenimiento crítico",
        )
        alert_repository.save(alert1)
        alert_repository.save(alert2)
        alert_repository.save(alert3)

        # Verify alerts exist before deletion
        alerts_before = alert_repository.get_by_vehicle_id("V-777")
        assert len(alerts_before) == 3

        use_case = DeleteVehicleUseCase(vehicle_repository=vehicle_repository)

        # Act
        use_case.execute(vehicle_id="V-777")

        # Assert - Vehicle deleted
        with pytest.raises(VehicleNotFoundException):
            vehicle_repository.get_by_id("V-777")

        # Assert - Alerts cascaded (deleted automatically)
        alerts_after = alert_repository.get_by_vehicle_id("V-777")
        assert len(alerts_after) == 0, "No orphan alerts should remain after vehicle deletion"
