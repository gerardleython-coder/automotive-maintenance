"""Tests for Vehicle entity following TDD approach."""
import pytest
from src.domain.entities.vehicle import Vehicle
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException


class TestVehicleCreation:
    """Test cases for Vehicle creation."""

    def test_create_vehicle_with_valid_data(self) -> None:
        """
        Given: Valid vehicle data
        When: Creating a new Vehicle instance
        Then: Vehicle should be created with correct attributes
        """
        # Arrange
        vehicle_id = "V-123"
        plate = "ABC-123"
        model = "Toyota Corolla"
        current_mileage = 5000

        # Act
        vehicle = Vehicle(
            id=vehicle_id,
            plate=plate,
            model=model,
            current_mileage=current_mileage
        )

        # Assert
        assert vehicle.id == vehicle_id
        assert vehicle.plate == plate
        assert vehicle.model == model
        assert vehicle.current_mileage == current_mileage


class TestVehicleMileageUpdate:
    """Test cases for Vehicle mileage update - HU-001 Escenario 2."""

    def test_update_mileage_with_lower_value_raises_exception(self) -> None:
        """
        Given: A vehicle with current mileage of 5,000 km
        When: Attempting to update mileage to 4,000 km (lower value)
        Then: System should raise InvalidMileageException
        """
        # Arrange
        vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota", current_mileage=5000)

        # Act & Assert
        with pytest.raises(InvalidMileageException):
            vehicle.update_mileage(4000)
