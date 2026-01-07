"""In-Memory Vehicle Repository - Infrastructure layer."""
from typing import Dict
from src.domain.ports.vehicle_repository import VehicleRepository
from src.domain.entities.vehicle import Vehicle


class InMemoryVehicleRepository(VehicleRepository):
    """In-memory implementation of VehicleRepository for testing and development."""

    def __init__(self) -> None:
        """Initialize repository with empty storage."""
        self._vehicles: Dict[str, Vehicle] = {}

    def get_by_id(self, vehicle_id: str) -> Vehicle:
        """
        Get vehicle by ID.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            Vehicle instance

        Raises:
            ValueError: If vehicle not found
        """
        if vehicle_id not in self._vehicles:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        return self._vehicles[vehicle_id]

    def save(self, vehicle: Vehicle) -> None:
        """
        Save vehicle to repository.

        Args:
            vehicle: Vehicle instance to save
        """
        self._vehicles[vehicle.id] = vehicle
