from app.models import ParkingLot


class AvailabilityService:

    def process_event(self, lot: ParkingLot, event_type: str, is_ada: bool = False):
        if event_type not in ("ENTER", "EXIT"):
            raise ValueError("Invalid event type")

        if event_type == "ENTER" and lot.status != "OPEN":
            raise ValueError("Cannot enter a closed lot")

        if is_ada:
            if event_type == "ENTER":
                if lot.get_open_ada_spots() == 0:
                    raise ValueError("No ADA spaces available")
                lot.ada_occupied += 1

            elif event_type == "EXIT":
                if lot.ada_occupied == 0:
                    raise ValueError("ADA occupancy cannot be negative")
                lot.ada_occupied -= 1

        else:
            if event_type == "ENTER":
                if lot.get_open_spots() == 0:
                    raise ValueError("No regular spaces available")
                lot.occupied += 1

            elif event_type == "EXIT":
                if lot.occupied == 0:
                    raise ValueError("Regular occupancy cannot be negative")
                lot.occupied -= 1

        return {
            "lot_id": lot.lot_id,
            "event": event_type,
            "is_ada": is_ada,
            "regular_occupied": lot.occupied,
            "ada_occupied": lot.ada_occupied,
            "regular_available": lot.get_open_spots(),
            "ada_available": lot.get_open_ada_spots()
        }

