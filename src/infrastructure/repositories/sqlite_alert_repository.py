"""SQLite implementation of AlertRepository - Infrastructure layer."""

from sqlalchemy.orm import Session

from src.domain.entities.maintenance_alert import MaintenanceAlert
from src.domain.ports.alert_repository import AlertRepository
from src.infrastructure.database.models import AlertModel


class SqliteAlertRepository(AlertRepository):
    """SQLite implementation of AlertRepository using SQLAlchemy."""

    def __init__(self, db_session: Session) -> None:
        """
        Initialize repository with database session.

        Args:
            db_session: SQLAlchemy database session
        """
        self._db = db_session

    def _to_entity(self, alert_model: AlertModel) -> MaintenanceAlert:
        """
        Convert AlertModel to MaintenanceAlert entity.

        Args:
            alert_model: SQLAlchemy model instance

        Returns:
            MaintenanceAlert domain entity
        """
        return MaintenanceAlert(
            id=alert_model.id,
            vehicle_id=alert_model.vehicle_id,
            alert_type=alert_model.alert_type,
            mileage=alert_model.mileage,
            timestamp=alert_model.timestamp,
        )

    def _to_model(self, alert: MaintenanceAlert) -> AlertModel:
        """
        Convert MaintenanceAlert entity to AlertModel.

        Args:
            alert: MaintenanceAlert domain entity

        Returns:
            AlertModel instance for persistence
        """
        return AlertModel(
            id=alert.id,
            vehicle_id=alert.vehicle_id,
            alert_type=alert.alert_type,
            mileage=alert.mileage,
            timestamp=alert.timestamp,
        )

    def save(self, alert: MaintenanceAlert) -> None:
        """
        Save alert to SQLite database.

        Args:
            alert: MaintenanceAlert entity to save
        """
        alert_model = self._to_model(alert)
        self._db.add(alert_model)
        self._db.commit()

    def get_all(self) -> list[MaintenanceAlert]:
        """
        Get all alerts from database.

        Returns:
            List of all MaintenanceAlert entities
        """
        raise NotImplementedError("To be implemented in next cycle")
