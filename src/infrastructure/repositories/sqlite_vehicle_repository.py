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

    def _to_entity(self, vehicle_model: VehicleModel) -> Vehicle:
        """
        Convert VehicleModel to Vehicle entity.

        Args:
            vehicle_model: SQLAlchemy model instance

        Returns:
            Vehicle domain entity
        """
        return Vehicle(
            id=vehicle_model.id,
            plate=vehicle_model.plate,
            model=vehicle_model.model,
            current_mileage=vehicle_model.current_mileage,
        )

    def _to_model(self, vehicle: Vehicle) -> VehicleModel:
        """
        Convert Vehicle entity to VehicleModel.

        Args:
            vehicle: Vehicle domain entity

        Returns:
            VehicleModel instance for persistence
        """
        return VehicleModel(
            id=vehicle.id,
            plate=vehicle.plate,
            model=vehicle.model,
            current_mileage=vehicle.current_mileage,
        )

    def _to_entities(self, vehicle_models: list[VehicleModel]) -> list[Vehicle]:
        """
        Convert list of VehicleModel to list of Vehicle entities.

        Args:
            vehicle_models: List of SQLAlchemy model instances

        Returns:
            List of Vehicle domain entities
        """
        return [self._to_entity(model) for model in vehicle_models]

    def save(self, vehicle: Vehicle) -> None:
        """
        Save vehicle to SQLite database.

        Args:
            vehicle: Vehicle entity to save
        """
        vehicle_model = self._to_model(vehicle)
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
        vehicle_model = (
            self._db.query(VehicleModel).filter_by(id=vehicle_id).first()
        )

        if vehicle_model is None:
            raise ValueError(f"Vehicle {vehicle_id} not found")

        return self._to_entity(vehicle_model)

    def get_all(self) -> list[Vehicle]:
        """
        Get all vehicles from database.

        Returns:
            List of all Vehicle entities
        """
        vehicle_models = self._db.query(VehicleModel).all()
        return self._to_entities(vehicle_models)
