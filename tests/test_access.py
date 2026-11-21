import pytest

from app.models import ParkingLot
from app.access import AccessService


@pytest.fixture
def student_lot():
    return ParkingLot(
        lot_id=1,
        name="Student Lot",
        capacity=30,
        occupied=10,
        ada_capacity=2,
        ada_occupied=0,
        status="OPEN",
        allowed_user_types=["STUDENT"]
    )


def test_valid_student_role():
    service = AccessService()

    assert service.validate_user_type("STUDENT") is True


def test_invalid_role():
    service = AccessService()

    with pytest.raises(ValueError, match="Invalid user type"):
        service.validate_user_type("DRIVER")


def test_student_allowed(student_lot):
    service = AccessService()

    assert service.can_access_lot(student_lot, "STUDENT") is True


def test_visitor_denied(student_lot):
    service = AccessService()

    assert service.can_access_lot(student_lot, "VISITOR") is False


def test_closed_lot_denied():
    lot = ParkingLot(
        lot_id=2,
        name="Closed Lot",
        capacity=20,
        occupied=5,
        ada_capacity=2,
        ada_occupied=0,
        status="CLOSED",
        allowed_user_types=["STUDENT"]
    )

    service = AccessService()

    assert service.can_access_lot(lot, "STUDENT") is False
