import pytest

from app.models import ParkingLot
from app.availability import AvailabilityService


@pytest.fixture
def parking_lot():
    return ParkingLot(
        lot_id=1,
        name="Test Lot",
        capacity=20,
        occupied=10,
        ada_capacity=2,
        ada_occupied=1,
        status="OPEN",
        allowed_user_types=["STUDENT"]
    )


def test_regular_vehicle_entry(parking_lot):
    service = AvailabilityService()

    result = service.process_event(parking_lot, "ENTER")

    assert result["regular_occupied"] == 11
    assert result["regular_available"] == 7


def test_regular_vehicle_exit(parking_lot):
    service = AvailabilityService()

    result = service.process_event(parking_lot, "EXIT")

    assert result["regular_occupied"] == 9
    assert result["regular_available"] == 9


def test_ada_vehicle_entry(parking_lot):
    service = AvailabilityService()

    result = service.process_event(parking_lot, "ENTER", is_ada=True)

    assert result["ada_occupied"] == 2
    assert result["ada_available"] == 0


def test_entry_into_full_lot():
    lot = ParkingLot(
        lot_id=2,
        name="Full Lot",
        capacity=10,
        occupied=9,
        ada_capacity=1,
        ada_occupied=1
    )

    service = AvailabilityService()

    with pytest.raises(ValueError, match="No regular spaces available"):
        service.process_event(lot, "ENTER")

    assert lot.occupied == 9


def test_exit_from_empty_lot():
    lot = ParkingLot(
        lot_id=3,
        name="Empty Lot",
        capacity=10,
        occupied=0,
        ada_capacity=1,
        ada_occupied=0
    )

    service = AvailabilityService()

    with pytest.raises(ValueError, match="Regular occupancy cannot be negative"):
        service.process_event(lot, "EXIT")

    assert lot.occupied == 0


def test_invalid_event(parking_lot):
    service = AvailabilityService()

    with pytest.raises(ValueError, match="Invalid event type"):
        service.process_event(parking_lot, "FLY")

    assert parking_lot.occupied == 10
    assert parking_lot.ada_occupied == 1
