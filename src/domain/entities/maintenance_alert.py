"""MaintenanceAlert entity for tracking vehicle maintenance alerts."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AlertType(Enum):
    """Types of maintenance alerts."""

    BASIC_MAINTENANCE = "basic_maintenance"  # Every 10,000 km
    MAJOR_MAINTENANCE = "major_maintenance"  # Every 50,000 km
    CRITICAL_THRESHOLD = "critical_threshold"  # At 100,000 km


@dataclass
class MaintenanceAlert:
    """Alert generated when vehicle reaches maintenance threshold."""

    id: str
    vehicle_id: str
    alert_type: AlertType
    mileage: int
    timestamp: datetime
