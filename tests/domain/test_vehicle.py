"""Tests for Vehicle entity following TDD approach."""
import pytest
from src.domain.entities.vehicle import Vehicle


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
