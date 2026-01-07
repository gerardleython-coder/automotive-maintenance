"""Vehicle entity - Domain model."""
from src.domain.exceptions.invalid_mileage_exception import InvalidMileageException


class Vehicle:
    """Vehicle entity representing a fleet vehicle."""

    MAX_MILEAGE = 1_000_000
    MAX_MILEAGE_INCREMENT = 50_000

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

        if new_mileage > self.MAX_MILEAGE:
            raise InvalidMileageException(
                f"El kilometraje {new_mileage} excede el límite máximo de {self.MAX_MILEAGE:,} km"
            )

        increment = new_mileage - self.current_mileage
        if increment > self.MAX_MILEAGE_INCREMENT:
            raise InvalidMileageException(
                f"El incremento de {increment:,} km excede el máximo permitido de {self.MAX_MILEAGE_INCREMENT:,} km"
            )

        self.current_mileage = new_mileage
