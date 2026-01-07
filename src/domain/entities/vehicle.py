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
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} debe ser mayor al actual {self.current_mileage}"
            )
        
        if new_mileage > 1000000:
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} excede el límite máximo de 1,000,000 km"
            )
        
        increment = new_mileage - self.current_mileage
        if increment > 50000:
            raise InvalidMileageException(
                f"El incremento de {increment} km excede el máximo permitido de 50,000 km"
            )

        self.current_mileage = new_mileage
