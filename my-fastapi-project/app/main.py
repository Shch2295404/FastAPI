from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms



app = FastAPI()

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

# class HotelsSearchArgs:
#     def __init__(
#         self,
#         location: str,
#         date_from: date,
#         date_to: date,
#         stars: Optional[int] = None,
#         has_spa: Optional[bool] = None,
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.has_spa = has_spa


# class SHotel(BaseModel):
#     address: str
#     name: str
#     stars: int


# @app.get("/hotels")
# def get_hotel(
#     search_args: HotelsSearchArgs = Depends(),
# ):
#     return search_args
