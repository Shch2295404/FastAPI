from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from fastapi import status

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SNewBooking, SBookingInfo
from app.users.models import Users
from app.users.dependesies import get_current_user
from app.exceptions import RoomCannotBeBookedException


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookingInfo]:
    """ 
    Получает список всех бронирований пользователя. Требуется аутентификация. 
    """
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
) -> SNewBooking:
    """
    Добавляет бронирование пользователя. Требуется аутентификация.
    """
    booking = await BookingDAO.add(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise RoomCannotBeBookedException
    return SNewBooking.model_validate(booking)


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, current_user: Users = Depends(get_current_user)):
    """
    Удаляет бронирование пользователя. Требуется аутентификация.
    """
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
