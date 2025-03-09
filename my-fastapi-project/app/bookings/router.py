from datetime import date
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo, SNewBooking
from app.bookings.service import BookingsService
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookingInfo]:
    """ 
    Получает список всех бронирований пользователя. Требуется аутентификация. 
    """
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    """
    Добавляет бронирование пользователя. Требуется аутентификация.
    """
    new_booking = await BookingsService.add_booking(
        booking,
        user,
    )
    send_booking_confirmation_email.delay(new_booking, user.email)
    return new_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
@version(1)
async def delete_booking(booking_id: int, current_user: Users = Depends(get_current_user)):
    """
    Удаляет бронирование пользователя. Требуется аутентификация.
    """
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
