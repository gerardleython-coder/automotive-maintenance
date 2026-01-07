"""Tests for InMemoryVehicleRepository following TDD approach."""
import pytest

from src.domain.entities.vehicle import Vehicle
from src.infrastructure.repositories.in_memory_vehicle_repository import InMemoryVehicleRepository


class TestInMemoryVehicleRepository:
    """Test cases for InMemoryVehicleRepository."""

    def test_save_and_retrieve_vehicle(self) -> None:
        """
        Given: An empty repository
        When: Saving a vehicle and retrieving it by ID
        Then: Should return the same vehicle with same attributes
        """
        # Arrange
        repository = InMemoryVehicleRepository()
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)

        # Act
        repository.save(vehicle)
        retrieved = repository.get_by_id("V-123")

        # Assert
        assert retrieved.id == "V-123"
        assert retrieved.plate == "ABC-123"
        assert retrieved.model == "Toyota"
        assert retrieved.current_mileage == 5000

    def test_update_existing_vehicle(self) -> None:
        """
        Given: A vehicle saved in repository
        When: Updating the vehicle and saving again
        Then: Should persist the updated values
        """
        # Arrange
        repository = InMemoryVehicleRepository()
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)
        repository.save(vehicle)

        # Act
        vehicle.update_mileage(10000)
        repository.save(vehicle)
        retrieved = repository.get_by_id("V-123")

        # Assert
        assert retrieved.current_mileage == 10000

    def test_get_by_id_raises_error_when_not_found(self) -> None:
        """
        Given: An empty repository
        When: Attempting to retrieve a non-existent vehicle
        Then: Should raise ValueError
        """
        # Arrange
        repository = InMemoryVehicleRepository()

        # Act & Assert
        with pytest.raises(ValueError, match="Vehicle V-999 not found"):
            repository.get_by_id("V-999")
