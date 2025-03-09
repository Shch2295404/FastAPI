import asyncio
from datetime import date, datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.params import Query
from fastapi_cache.decorator import cache

from app.exceptions import DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)

@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    """Получает список **всех отелей**, расположенных в определенной локации со свободными номерами."""
    await asyncio.sleep(3)
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    """Получает информацию об отеле по его id."""
    return await HotelDAO.find_one_or_none(id=hotel_id)
