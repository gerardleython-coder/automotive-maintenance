"""Vehicle entity - Domain model."""


class Vehicle:
    """Vehicle entity representing a fleet vehicle."""

    def __init__(self, id: str, plate: str, model: str, current_mileage: int):
        self.id = id
        self.plate = plate
        self.model = model
        self.current_mileage = current_mileage
