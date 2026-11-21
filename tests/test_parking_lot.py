import pytest
from app.models import ParkingLot


def test_normal_availability():
    lot = ParkingLot(
        lot_id=1,
        name="Lot A",
        capacity=120,
        occupied=70,
        ada_capacity=6,
        ada_occupied=2
    )

    assert lot.get_open_spots() == 44
    assert lot.get_open_ada_spots() == 4


def test_full_parking_lot():
    lot = ParkingLot(
        lot_id=2,
        name="Full Lot",
        capacity=20,
        occupied=18,
        ada_capacity=2,
        ada_occupied=2
    )

    assert lot.get_open_spots() == 0
    assert lot.get_open_ada_spots() == 0
    assert lot.is_full() is True


def test_occupancy_exceeds_regular_capacity():
    with pytest.raises(ValueError):
        ParkingLot(
            lot_id=3,
            name="Overfilled Lot",
            capacity=20,
            occupied=19,
            ada_capacity=2,
            ada_occupied=0
        )


def test_negative_occupancy():
    with pytest.raises(ValueError):
        ParkingLot(
            lot_id=4,
            name="Invalid Lot",
            capacity=20,
            occupied=-1,
            ada_capacity=2,
            ada_occupied=0
        )


def test_user_eligibility():
    lot = ParkingLot(
        lot_id=5,
        name="Student Lot",
        capacity=30,
        occupied=10,
        ada_capacity=2,
        ada_occupied=0,
        allowed_user_types=["STUDENT"]
    )

    assert lot.is_user_allowed("STUDENT") is True
    assert lot.is_user_allowed("VISITOR") is False
