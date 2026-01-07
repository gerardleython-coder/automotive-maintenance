"""Basic Maintenance Strategy - every 10,000 km."""
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy
from src.domain.entities.maintenance_alert import AlertType


class BasicMaintenanceStrategy(MaintenanceStrategy):
    """Strategy for basic maintenance every 10,000 km."""

    INTERVAL = 10_000

    def _calculate_threshold(self, mileage: int) -> int:
        """
        Calculate the maintenance threshold for given mileage.

        Args:
            mileage: Current mileage value

        Returns:
            The last crossed threshold (multiple of INTERVAL)
        """
        return (mileage // self.INTERVAL) * self.INTERVAL

    def should_generate_alert(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Check if vehicle crosses a 10,000 km threshold.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if crosses 10,000 km threshold, False otherwise
        """
        old_threshold = self._calculate_threshold(old_mileage)
        new_threshold = self._calculate_threshold(new_mileage)
        return new_threshold > old_threshold

    def get_alert_type(self) -> AlertType:
        """Return BASIC_MAINTENANCE alert type."""
        return AlertType.BASIC_MAINTENANCE
