from dataclasses import dataclass, field
from typing import List


@dataclass
class ParkingLot:
    lot_id: int
    name: str
    capacity: int
    occupied: int
    ada_capacity: int
    ada_occupied: int
    status: str = "OPEN"
    allowed_user_types: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.capacity < 0 or self.occupied < 0:
            raise ValueError("Capacity and occupancy cannot be negative")

        if self.occupied > self.capacity - self.ada_capacity:
            raise ValueError("Occupancy cannot exceed capacity")

        if self.ada_capacity < 0 or self.ada_occupied < 0:
            raise ValueError("ADA values cannot be negative")

        if self.ada_occupied > self.ada_capacity:
            raise ValueError("ADA occupancy cannot exceed ADA capacity")

        if self.ada_capacity > self.capacity:
            raise ValueError("ADA capacity cannot exceed total capacity")

        if self.occupied + self.ada_occupied > self.capacity:
            raise ValueError("Combined occupancy cannot exceed total capacity")

        if self.status not in ("OPEN", "CLOSED"):
            raise ValueError("Invalid parking lot status")

    def get_open_spots(self):
        regular_capacity = self.capacity - self.ada_capacity
        return regular_capacity - self.occupied

    def get_open_ada_spots(self):
        return self.ada_capacity - self.ada_occupied

    def is_full(self):
        return (
            self.get_open_spots() == 0
            and self.get_open_ada_spots() == 0
        )

    def is_user_allowed(self, user_type):
        return (
            self.status == "OPEN"
            and user_type in self.allowed_user_types
        )

