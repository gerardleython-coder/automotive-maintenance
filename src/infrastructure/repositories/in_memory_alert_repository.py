"""In-Memory Alert Repository - Infrastructure layer."""
from typing import List
from src.domain.ports.alert_repository import AlertRepository
from src.domain.entities.maintenance_alert import MaintenanceAlert


class InMemoryAlertRepository(AlertRepository):
    """
    In-memory implementation of AlertRepository for testing and development.

    This implementation stores alerts in memory and is suitable for
    testing and development environments. For production, use a persistent
    storage implementation.
    """

    def __init__(self) -> None:
        """Initialize repository with empty storage."""
        self._alerts: List[MaintenanceAlert] = []

    def save(self, alert: MaintenanceAlert) -> None:
        """
        Save alert to repository.

        Args:
            alert: MaintenanceAlert instance to save
        """
        self._alerts.append(alert)

    def get_all(self) -> List[MaintenanceAlert]:
        """
        Get all alerts from repository.

        Returns:
            List of all MaintenanceAlert instances
        """
        return self._alerts.copy()
