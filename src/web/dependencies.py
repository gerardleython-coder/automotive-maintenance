"""Dependency injection configuration."""
from src.infrastructure.repositories.in_memory_vehicle_repository import InMemoryVehicleRepository
from src.infrastructure.repositories.in_memory_alert_repository import InMemoryAlertRepository
from src.domain.entities.vehicle import Vehicle


# Singleton instances
_vehicle_repository = InMemoryVehicleRepository()
_alert_repository = InMemoryAlertRepository()


def get_vehicle_repository() -> InMemoryVehicleRepository:
    """Get vehicle repository instance."""
    return _vehicle_repository


def get_alert_repository() -> InMemoryAlertRepository:
    """Get alert repository instance."""
    return _alert_repository


def initialize_test_data() -> None:
    """Initialize test data for development."""
    test_vehicle = Vehicle(id="V-123", plate="ABC-123", model="Toyota Corolla", current_mileage=5000)
    _vehicle_repository.save(test_vehicle)
