"""Use case for registering a new vehicle in the system."""

from src.domain.entities.vehicle import Vehicle
from src.domain.ports.vehicle_repository import VehicleRepository


class RegisterVehicleUseCase:
    """Use case for registering a new vehicle."""

    def __init__(self, vehicle_repository: VehicleRepository):
        """Initialize use case with repository dependency."""
        self._vehicle_repository = vehicle_repository

    def execute(
        self, vehicle_id: str, plate: str, model: str, initial_mileage: int
    ) -> Vehicle:
        """
        Register a new vehicle in the system.

        Args:
            vehicle_id: Unique identifier for the vehicle
            plate: License plate number
            model: Vehicle model name
            initial_mileage: Starting mileage value

        Returns:
            The registered vehicle entity

        Raises:
            ValueError: If vehicle with same ID already exists
        """
        # Validate vehicle ID doesn't exist
        try:
            self._vehicle_repository.get_by_id(vehicle_id)
            raise ValueError(f"Ya existe un vehículo con ID {vehicle_id}")
        except ValueError as e:
            # If error message contains "Ya existe", re-raise it
            if "Ya existe" in str(e):
                raise
            # Otherwise, vehicle doesn't exist (expected), continue

        # Create new vehicle entity
        vehicle = Vehicle(
            id=vehicle_id, plate=plate, model=model, current_mileage=initial_mileage
        )

        # Save to repository
        self._vehicle_repository.save(vehicle)

        return vehicle
