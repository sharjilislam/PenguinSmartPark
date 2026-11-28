import pytest

from app.models import ParkingLot


def test_component_model_reports_regular_and_ada_availability():
    lot = ParkingLot(1, "Lot A", 20, 10, 2, 1, allowed_user_types=["STUDENT"])
    assert lot.get_open_spots() == 8
    assert lot.get_open_ada_spots() == 1


def test_component_model_reports_full_when_all_spaces_are_used():
    lot = ParkingLot(2, "Full Lot", 10, 8, 2, 2, allowed_user_types=["STUDENT"])
    assert lot.is_full() is True


def test_component_model_rejects_negative_ada_capacity():
    with pytest.raises(ValueError, match="ADA values cannot be negative"):
        ParkingLot(3, "Invalid Lot", 10, 0, -1, 0)
