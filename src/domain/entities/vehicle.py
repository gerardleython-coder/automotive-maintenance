"""Vehicle entity - Domain model."""


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
