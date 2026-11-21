from app.models import ParkingLot
from app.access import AccessService
from app.availability import AvailabilityService
from app.recommendation import RecommendationService


def make_lots():
    return [
        ParkingLot(
            lot_id=1,
            name="Student Lot A",
            capacity=20,
            occupied=10,
            ada_capacity=2,
            ada_occupied=0,
            allowed_user_types=["STUDENT"]
        ),
        ParkingLot(
            lot_id=2,
            name="Student Lot B",
            capacity=20,
            occupied=5,
            ada_capacity=2,
            ada_occupied=0,
            allowed_user_types=["STUDENT"]
        ),
        ParkingLot(
            lot_id=3,
            name="Visitor Lot",
            capacity=20,
            occupied=5,
            ada_capacity=2,
            ada_occupied=0,
            allowed_user_types=["VISITOR"]
        )
    ]


def test_component_normal_recommendation():
    lots = make_lots()
    access = AccessService()
    recommendation = RecommendationService()

    assert access.can_access_lot(lots[0], "STUDENT") is True
    assert access.can_access_lot(lots[2], "STUDENT") is False

    result = recommendation.recommend(
        lots,
        "STUDENT",
        {1: 3, 2: 6, 3: 1}
    )

    assert [item["lot_id"] for item in result] == [1, 2]
    assert result[0]["walking_minutes"] == 3


def test_component_recommendation_updates_after_entry():
    lots = make_lots()
    availability = AvailabilityService()
    recommendation = RecommendationService()

    # Leave only one regular space in Lot A.
    lots[0].occupied = 17

    before = recommendation.recommend(
        lots, "STUDENT", {1: 3, 2: 6, 3: 1}
    )

    assert before[0]["lot_id"] == 1
    assert before[0]["regular_available"] == 1

    # Simulate the last regular space being occupied.
    event = availability.process_event(lots[0], "ENTER")

    assert event["regular_available"] == 0

    after = recommendation.recommend(
        lots, "STUDENT", {1: 3, 2: 6, 3: 1}
    )

    assert [item["lot_id"] for item in after] == [2]


def test_component_unauthorized_user_excluded():
    lots = make_lots()
    access = AccessService()
    recommendation = RecommendationService()

    assert access.can_access_lot(lots[0], "VISITOR") is False
    assert access.can_access_lot(lots[2], "VISITOR") is True

    result = recommendation.recommend(
        lots,
        "VISITOR",
        {1: 3, 2: 6, 3: 1}
    )

    assert [item["lot_id"] for item in result] == [3]
    assert result[0]["name"] == "Visitor Lot"
