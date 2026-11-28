import pytest

from app.access import AccessService
from app.models import ParkingLot


def make_lot(status="OPEN", allowed=None):
    return ParkingLot(1, "Campus Lot", 20, 5, 2, 0, status=status, allowed_user_types=allowed or ["STUDENT"])


def test_component_access_allows_eligible_user_in_open_lot():
    assert AccessService().can_access_lot(make_lot(), "STUDENT") is True


def test_component_access_denies_user_not_in_lot_role_list():
    assert AccessService().can_access_lot(make_lot(), "VISITOR") is False


def test_component_access_rejects_invalid_user_type():
    with pytest.raises(ValueError, match="Invalid user type"):
        AccessService().can_access_lot(make_lot(), "DRIVER")
