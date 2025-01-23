from app.bookings.models import Bookings
from app.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings
