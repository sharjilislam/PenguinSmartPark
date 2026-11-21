import pytest

from app.models import ParkingLot
from app.recommendation import RecommendationService


def make_lot(lot_id, occupied=5, status="OPEN", allowed=None):
    if allowed is None:
        allowed = ["STUDENT"]

    return ParkingLot(
        lot_id=lot_id,
        name=f"Lot {lot_id}",
        capacity=20,
        occupied=occupied,
        ada_capacity=2,
        ada_occupied=0,
        status=status,
        allowed_user_types=allowed
    )


def test_returns_closest_three_lots():
    lots = [make_lot(i) for i in range(1, 6)]
    walking_times = {1: 8, 2: 3, 3: 5, 4: 1, 5: 6}

    result = RecommendationService().recommend(
        lots, "STUDENT", walking_times
    )

    assert [lot["lot_id"] for lot in result] == [4, 2, 3]
    assert len(result) == 3


def test_excludes_unauthorized_lot():
    lots = [
        make_lot(1, allowed=["VISITOR"]),
        make_lot(2, allowed=["STUDENT"])
    ]

    result = RecommendationService().recommend(
        lots, "STUDENT", {1: 1, 2: 5}
    )

    assert [lot["lot_id"] for lot in result] == [2]


def test_excludes_full_lot():
    lots = [
        make_lot(1, occupied=18),
        make_lot(2, occupied=5)
    ]

    result = RecommendationService().recommend(
        lots, "STUDENT", {1: 1, 2: 4}
    )

    assert [lot["lot_id"] for lot in result] == [2]


def test_excludes_closed_lot():
    lots = [
        make_lot(1, status="CLOSED"),
        make_lot(2)
    ]

    result = RecommendationService().recommend(
        lots, "STUDENT", {1: 1, 2: 6}
    )

    assert [lot["lot_id"] for lot in result] == [2]


def test_invalid_user_type():
    lots = [make_lot(1)]

    with pytest.raises(ValueError, match="Invalid user type"):
        RecommendationService().recommend(
            lots, "DRIVER", {1: 3}
        )


def test_invalid_walking_time():
    lots = [make_lot(1)]

    with pytest.raises(ValueError, match="Invalid walking time"):
        RecommendationService().recommend(
            lots, "STUDENT", {1: -5}
        )
