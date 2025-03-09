from datetime import date

from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):

        """
        Получает список **всех отелей**, расположенных в определенной локации со свободными номерами.
        """

        """
        WITH booked_rooms AS (
            SELECT 
                b.room_id, 
                COUNT(b.room_id) AS rooms_booked
            FROM bookings b
            WHERE 
                b.date_to >= '2023-05-15' 
                AND b.date_from <= '2023-06-20' -- Проверка пересечения дат
            GROUP BY b.room_id
        ),
        booked_hotels AS (
            SELECT 
                r.hotel_id, 
                SUM(GREATEST(r.quantity - COALESCE(br.rooms_booked, 0), 0)) AS rooms_left -- Учитываем, что rooms_left не может быть отрицательным
            FROM rooms r
            LEFT JOIN booked_rooms br ON br.room_id = r.id
            GROUP BY r.hotel_id
        )
        SELECT 
            h.id, 
            h.name, 
            h.location, 
            h.services, 
            h.rooms_quantity, 
            h.image_id,
            bh.rooms_left
        FROM hotels h
        JOIN booked_hotels bh ON bh.hotel_id = h.id -- INNER JOIN, т.к. нужны только отели с доступными номерами
        WHERE 
            bh.rooms_left > 0
            AND h.location ILIKE '%алтай%'; -- Поддержка частичного поиска
        """

        # Определяем количество занятых номеров
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                and_(
                    Bookings.date_to >= date_from,
                    Bookings.date_from <= date_to
                )
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        # Подсчет доступных номеров в каждом отеле
        booked_hotels = (
            select(
                Rooms.hotel_id,
                func.sum(
                    func.greatest(Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0), 0)
                ).label("rooms_left"),
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

        # Запрос на выборку отелей с доступными номерами
        get_hotels_with_rooms = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.ilike(f"%{location}%"),  # Используем `ILIKE` для нечувствительного поиска
                )
            )
        )

        # Выполнение запроса
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
            
