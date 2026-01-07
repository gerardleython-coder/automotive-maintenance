"""SQLite implementation of VehicleRepository - Infrastructure layer."""

from sqlalchemy.orm import Session

from src.domain.entities.vehicle import Vehicle
from src.domain.ports.vehicle_repository import VehicleRepository
from src.infrastructure.database.models import VehicleModel


class SqliteVehicleRepository(VehicleRepository):
    """SQLite implementation of VehicleRepository using SQLAlchemy."""

    def __init__(self, db_session: Session) -> None:
        """
        Initialize repository with database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self._db = db_session

    def save(self, vehicle: Vehicle) -> None:
        """
        Save vehicle to SQLite database.

        Args:
            vehicle: Vehicle entity to save
        """
        vehicle_model = VehicleModel(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage,
        )
        self._db.merge(vehicle_model)
        self._db.commit()

    def get_by_id(self, vehicle_id: str) -> Vehicle:
        """
        Get vehicle by ID from database.

        Args:
            vehicle_id: Unique identifier of the vehicle

        Returns:
            Vehicle entity

        Raises:
            ValueError: If vehicle not found
        """
        raise NotImplementedError("To be implemented in next cycle")
