from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.access import AccessService
from app.availability import AvailabilityService
from app.models import ParkingLot
from app.recommendation import RecommendationService

app = FastAPI(
    title="Penguin SmartPark",
    description="Smart parking recommendation system for Youngstown State University",
    version="0.1.0",
)


class ParkingEvent(BaseModel):
    event_type: str
    is_ada: bool = False


class RecommendationRequest(BaseModel):
    user_type: str
    walking_times: dict[int, float]
    limit: int = Field(default=3, ge=1)


def create_demo_lots():
    return [
        ParkingLot(1, "Student Lot A", 20, 17, 2, 0, allowed_user_types=["STUDENT"]),
        ParkingLot(2, "Student Lot B", 20, 5, 2, 0, allowed_user_types=["STUDENT", "FACULTY_STAFF"]),
        ParkingLot(3, "Visitor Lot", 20, 5, 2, 0, allowed_user_types=["VISITOR"]),
    ]


def reset_demo_lots():
    """Reset the in-memory demo data for a new application run or test."""
    app.state.lots = create_demo_lots()


reset_demo_lots()


def get_lot(lot_id: int):
    for lot in app.state.lots:
        if lot.lot_id == lot_id:
            return lot
    raise HTTPException(status_code=404, detail="Parking lot not found")


def lot_summary(lot: ParkingLot):
    return {
        "lot_id": lot.lot_id,
        "name": lot.name,
        "status": lot.status,
        "regular_available": lot.get_open_spots(),
        "ada_available": lot.get_open_ada_spots(),
        "allowed_user_types": lot.allowed_user_types,
    }


@app.get("/")
def home():
    return {"project": "Penguin SmartPark", "message": "Welcome to Penguin SmartPark!", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Penguin SmartPark Backend"}


@app.get("/lots")
def list_lots():
    return [lot_summary(lot) for lot in app.state.lots]


@app.get("/lots/{lot_id}/access")
def check_access(lot_id: int, user_type: str):
    try:
        allowed = AccessService().can_access_lot(get_lot(lot_id), user_type)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"lot_id": lot_id, "user_type": user_type, "allowed": allowed}


@app.post("/lots/{lot_id}/events")
def process_event(lot_id: int, event: ParkingEvent):
    try:
        return AvailabilityService().process_event(get_lot(lot_id), event.event_type, event.is_ada)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/recommendations")
def get_recommendations(request: RecommendationRequest):
    try:
        return RecommendationService().recommend(app.state.lots, request.user_type, request.walking_times, request.limit)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
