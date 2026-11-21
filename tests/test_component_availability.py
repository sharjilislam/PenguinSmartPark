import pytest

from app.models import ParkingLot
from app.availability import AvailabilityService


def make_lot():
    return ParkingLot(
        lot_id=1,
        name="Campus Lot A",
        capacity=30,
        occupied=10,
        ada_capacity=2,
        ada_occupied=1,
        status="OPEN",
        allowed_user_types=["STUDENT"]
    )


def test_component_vehicle_entry_updates_availability():
    lot = make_lot()
    service = AvailabilityService()

    before = lot.get_open_spots()
    result = service.process_event(lot, "ENTER")

    assert before == 18
    assert result["regular_available"] == 17
    assert lot.get_open_spots() == 17
    assert lot.occupied == 11


def test_component_vehicle_exit_updates_availability():
    lot = make_lot()
    service = AvailabilityService()

    before = lot.get_open_spots()
    result = service.process_event(lot, "EXIT")

    assert before == 18
    assert result["regular_available"] == 19
    assert lot.get_open_spots() == 19
    assert lot.occupied == 9


def test_component_invalid_event_preserves_state():
    lot = make_lot()
    service = AvailabilityService()

    original_occupied = lot.occupied
    original_available = lot.get_open_spots()

    with pytest.raises(ValueError, match="Invalid event type"):
        service.process_event(lot, "FLY")

    assert lot.occupied == original_occupied
    assert lot.get_open_spots() == original_available
