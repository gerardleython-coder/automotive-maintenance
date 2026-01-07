"""Tests for SqliteVehicleRepository - Infrastructure layer."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.vehicle import Vehicle
from src.infrastructure.database.models import Base
from src.infrastructure.repositories.sqlite_vehicle_repository import (
    SqliteVehicleRepository,
)


@pytest.fixture
def test_db():
    """Create clean in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def repository(test_db):
    """Create repository instance with test database."""
    return SqliteVehicleRepository(test_db)


class TestSqliteVehicleRepository:
    """Test suite for SqliteVehicleRepository."""

    def test_save_vehicle_to_database(self, repository, test_db):
        """
        Test saving a vehicle to SQLite database.

        Given a valid vehicle entity
        When save() is called
        Then the vehicle should be persisted in the database
        """
        # Arrange
        vehicle = Vehicle(
            id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000
        )

        # Act
        repository.save(vehicle)

        # Assert
        from src.infrastructure.database.models import VehicleModel

        saved_vehicle = test_db.query(VehicleModel).filter_by(id="V-123").first()
        assert saved_vehicle is not None
        assert saved_vehicle.id == "V-123"
        assert saved_vehicle.plate == "ABC-123"
        assert saved_vehicle.model == "Toyota Corolla"
        assert saved_vehicle.current_mileage == 5000

    def test_get_vehicle_by_id_from_database(self, repository, test_db):
        """
        Test retrieving a vehicle by ID from SQLite database.

        Given a vehicle saved in the database
        When get_by_id() is called with the vehicle ID
        Then the vehicle entity should be returned with correct data
        """
        # Arrange
        from src.infrastructure.database.models import VehicleModel

        vehicle_model = VehicleModel(
            id="V-456", plate="XYZ-789", model="Honda Civic", current_mileage=15000
        )
        test_db.add(vehicle_model)
        test_db.commit()

        # Act
        vehicle = repository.get_by_id("V-456")

        # Assert
        assert vehicle is not None
        assert vehicle.id == "V-456"
        assert vehicle.plate == "XYZ-789"
        assert vehicle.model == "Honda Civic"
        assert vehicle.current_mileage == 15000
