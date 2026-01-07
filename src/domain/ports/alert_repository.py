"""Alert Repository port - following DIP."""
from abc import ABC, abstractmethod

from src.domain.entities.maintenance_alert import MaintenanceAlert


class AlertRepository(ABC):
    """Interface for alert repository following DIP."""

    @abstractmethod
    def save(self, alert: MaintenanceAlert) -> None:
        """
        Save alert to repository.

        Args:
            alert: MaintenanceAlert instance to save
        """
        pass
