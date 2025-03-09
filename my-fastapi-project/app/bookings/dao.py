from datetime import date

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger



class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(cls, user_id: int):
        """
        Получает список всех бронирований пользователя с информацией о номерах.
        """

        """
        SELECT
            b.room_id,
            b.user_id,
            b.date_from,
            b.date_to,
            b.price,
            b.total_cost,
            b.total_days,
            r.image_id,
            r.name,
            r.description,
            r.services
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        WHERE b.user_id = 3;
        """

        get_bookings = (
            select(
                Bookings.__table__.columns,
                Rooms.__table__.columns,
            )
            .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
            .where(Bookings.user_id == user_id)
        )

        async with async_session_maker() as session:
            bookings = await session.execute(get_bookings)
            return bookings.mappings().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from <= '2023-06-20') AND (date_to >= '2023-05-15')
        )
        """
        try:
            async with async_session_maker() as session:
                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.room_id == room_id,
                        and_(
                            Bookings.date_to >= date_from,
                            Bookings.date_from <= date_to
                        )
                    )
                ).cte("booked_rooms")
                """
                SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = 1
                GROUP BY rooms.quantity, booked_rooms.room_id
                """

                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )

                # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()

                if None > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = insert(Bookings).values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    ).returning(Bookings)

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg = msg + ": Cannot add booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to
            }
            logger.error(msg, exc_info=True, extra=extra)
            
