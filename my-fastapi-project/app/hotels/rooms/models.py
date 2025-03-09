from typing import TYPE_CHECKING

from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в 
    # PyCharm и VSCode
    from bookings.models import Bookings
    from hotels.models import Hotels

# class Rooms(Base):
#    __tablename__ = "rooms"

#    id = Column(Integer, primary_key=True, nullable=False)
#    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
#    name = Column(String, nullable=False)
#    description = Column(String, nullable=True)
#    price = Column(Integer, nullable=False)
#    services = Column(JSON, nullable=True)
#    quantity = Column(Integer, nullable=False)
#    image_id = Column(Integer)

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f"Номер {self.name}"
