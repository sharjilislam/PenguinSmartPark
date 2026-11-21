from app.models import ParkingLot


class AccessService:

    VALID_USER_TYPES = ("STUDENT", "FACULTY_STAFF", "VISITOR")

    def validate_user_type(self, user_type):
        if user_type not in self.VALID_USER_TYPES:
            raise ValueError("Invalid user type")

        return True

    def can_access_lot(self, lot: ParkingLot, user_type):
        self.validate_user_type(user_type)

        if not isinstance(lot, ParkingLot):
            raise ValueError("Invalid parking lot")

        return lot.is_user_allowed(user_type)
