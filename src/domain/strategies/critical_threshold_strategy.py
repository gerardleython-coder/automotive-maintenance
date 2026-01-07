"""Critical Threshold Strategy - alert at 100,000 km."""
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy
from src.domain.entities.maintenance_alert import AlertType


class CriticalThresholdStrategy(MaintenanceStrategy):
    """Strategy for critical threshold at 100,000 km."""

    CRITICAL_THRESHOLD = 100_000
    INTERVAL = CRITICAL_THRESHOLD  # Required by base class

    def should_generate_alert(self, old_mileage: int, new_mileage: int) -> bool:
        """
        Check if vehicle crosses the critical 100,000 km threshold.

        Args:
            old_mileage: Previous mileage value
            new_mileage: New mileage value

        Returns:
            True if crosses 100,000 km threshold (only once), False otherwise
        """
        return old_mileage < self.CRITICAL_THRESHOLD <= new_mileage

    def get_alert_type(self) -> AlertType:
        """Return CRITICAL_THRESHOLD alert type."""
        return AlertType.CRITICAL_THRESHOLD
