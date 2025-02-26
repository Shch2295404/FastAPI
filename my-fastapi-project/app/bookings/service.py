from app.bookings.dao import BookingDAO
from app.bookings.schemas import SNewBooking
from app.exceptions import RoomCannotBeBookedException
from app.users.models import Users


class BookingsService:
    @classmethod
    async def add_booking(
        cls,
        booking: SNewBooking,
        user: Users,
    ):
        booking = await BookingDAO.add(
            user.id, 
            booking.room_id, 
            booking.date_from, 
            booking.date_to,
        )
        if not booking:
            raise RoomCannotBeBookedException
        booking = SNewBooking.model_validate(booking)
        return booking