"""Update Vehicle Mileage Use Case - Application layer."""
from datetime import datetime
from typing import List
from src.domain.ports.vehicle_repository import VehicleRepository
from src.domain.ports.alert_repository import AlertRepository
from src.domain.strategies.maintenance_strategy import MaintenanceStrategy
from src.domain.strategies.basic_maintenance_strategy import BasicMaintenanceStrategy
from src.domain.entities.maintenance_alert import MaintenanceAlert


class UpdateVehicleMileageUseCase:
    """Use case for updating vehicle mileage following SRP."""

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        alert_repository: AlertRepository,
        strategies: List[MaintenanceStrategy] = None
    ) -> None:
        """
        Initialize use case with dependencies.

        Args:
            vehicle_repository: Repository for vehicle persistence
            alert_repository: Repository for alert persistence
            strategies: List of maintenance strategies (defaults to BasicMaintenanceStrategy)
        """
        self._vehicle_repository = vehicle_repository
        self._alert_repository = alert_repository
        self._strategies = strategies or [BasicMaintenanceStrategy()]

    def execute(self, vehicle_id: str, new_mileage: int) -> None:
        """
        Execute the use case to update vehicle mileage.

        Args:
            vehicle_id: Unique identifier of the vehicle
            new_mileage: New mileage value

        Raises:
            InvalidMileageException: If new mileage is invalid
            ValueError: If vehicle not found
        """
        # Get vehicle
        vehicle = self._vehicle_repository.get_by_id(vehicle_id)
        
        # Store old mileage for strategy evaluation
        old_mileage = vehicle.current_mileage
        
        # Update mileage (domain validation happens here)
        vehicle.update_mileage(new_mileage)
        
        # Check maintenance strategies and generate alerts
        for strategy in self._strategies:
            if strategy.should_generate_alert(old_mileage, new_mileage):
                alert = MaintenanceAlert(
                    id=f"A-{vehicle_id}-{new_mileage}-{strategy.get_alert_type().value}",
                    vehicle_id=vehicle_id,
                    alert_type=strategy.get_alert_type(),
                    mileage=new_mileage,
                    timestamp=datetime.now()
                )
                self._alert_repository.save(alert)
        
        # Persist updated vehicle
        self._vehicle_repository.save(vehicle)
