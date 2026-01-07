"""Tests for UpdateVehicleMileageUseCase following TDD approach."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.application.use_cases.update_vehicle_mileage_use_case import UpdateVehicleMileageUseCase
from src.domain.entities.maintenance_alert import AlertType
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException
from src.infrastructure.database.models import Base
from src.infrastructure.repositories.sqlite_alert_repository import SqliteAlertRepository
from src.infrastructure.repositories.sqlite_vehicle_repository import SqliteVehicleRepository


@pytest.fixture
def test_db():
    """Create test database with persistent SQLite."""
    # Use test database file
    engine = create_engine("sqlite:///test_maintenance.db")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine)
    session = session_local()

    yield session

    # Cleanup after test
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def vehicle_repo(test_db):
    """Create vehicle repository with test database."""
    return SqliteVehicleRepository(test_db)


@pytest.fixture
def alert_repo(test_db):
    """Create alert repository with test database."""
    return SqliteAlertRepository(test_db)


class TestUpdateVehicleMileageUseCase:
    """Test cases for UpdateVehicleMileageUseCase."""

    def test_update_mileage_successfully(
        self, vehicle_repo, alert_repo
    ) -> None:
        """
        Given: A vehicle with 5,000 km
        When: Updating mileage to 8,000 km
        Then: Vehicle mileage should be updated
        And: Vehicle should be persisted
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000
        )
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

    def test_update_mileage_with_invalid_value_raises_exception(
        self, vehicle_repo, alert_repo
    ) -> None:
        """
        Given: A vehicle with 5,000 km
        When: Attempting to update with invalid mileage (4,000 km)
        Then: Should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000
        )
        vehicle_repo.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repo,
            alert_repository=alert_repo
        )

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            use_case.execute(vehicle_id="V-123", new_mileage=4000)

    def test_update_mileage_crossing_10k_threshold_generates_alert(
        self, vehicle_repo, alert_repo
    ) -> None:
        """
        Given: A vehicle with 5,000 km and basic maintenance strategy
        When: Updating mileage to 10,001 km
        Then: Should generate and persist a basic maintenance alert
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000
        )
        vehicle_repo.save(vehicle)

        use_case = UpdateVehicleMileageUseCase(
            vehicle_repository=vehicle_repo,
            alert_repository=alert_repo
        )

        # Act
        use_case.execute(vehicle_id="V-123", new_mileage=10001)

        # Assert
        alerts = alert_repo.get_all()
        assert len(alerts) == 1
        alert = alerts[0]
        assert alert.vehicle_id == "V-123"
        assert alert.mileage == 10001
        assert alert.alert_type == AlertType.BASIC_MAINTENANCE
