from app.models import ParkingLot


class RecommendationService:

    def recommend(self, lots, user_type, walking_times, limit=3):
        if user_type not in ("STUDENT", "FACULTY_STAFF", "VISITOR"):
            raise ValueError("Invalid user type")

        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise ValueError("Limit must be a positive integer")

        recommendations = []

        for lot in lots:
            if not isinstance(lot, ParkingLot):
                raise ValueError("Invalid parking lot")

            if not lot.is_user_allowed(user_type):
                continue

            if lot.get_open_spots() <= 0:
                continue

            if lot.lot_id not in walking_times:
                continue

            minutes = walking_times[lot.lot_id]

            if isinstance(minutes, bool) or not isinstance(minutes, (int, float)) or not 0 <= minutes < float("inf"):
                raise ValueError("Invalid walking time")

            recommendations.append({
                "lot_id": lot.lot_id,
                "name": lot.name,
                "walking_minutes": minutes,
                "regular_available": lot.get_open_spots(),
                "ada_available": lot.get_open_ada_spots()
            })

        recommendations.sort(
            key=lambda item: (item["walking_minutes"], item["lot_id"])
        )

        return recommendations[:limit]
