"""Vehicle entity - Domain model."""
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException


class Vehicle:
    """Vehicle entity representing a fleet vehicle."""

    def __init__(self, id: str, plate: str, model: str, current_mileage: int) -> None:
        """
        Initialize a Vehicle instance.

        Args:
            id: Unique identifier for the vehicle
            plate: License plate number
            model: Vehicle model name
            current_mileage: Current mileage in kilometers
        """
        self.id = id
        self.plate = plate
        self.model = model
        self.current_mileage = current_mileage

    def update_mileage(self, new_mileage: int) -> None:
        """
        Update vehicle mileage.

        Args:
            new_mileage: New mileage value

        Raises:
            InvalidMileageException: If new mileage is not greater than current
        """
        if new_mileage <= self.current_mileage:
            raise InvalidMileageException()
        
        self.current_mileage = new_mileage
