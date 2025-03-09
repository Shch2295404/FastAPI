import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 200),
    (4, "2030-05-01", "2030-05-15", 4, 200),
    (4, "2030-05-01", "2030-05-15", 5, 200),
    (4, "2030-05-01", "2030-05-15", 6, 200),
    (4, "2030-05-01", "2030-05-15", 7, 200),
    (4, "2030-05-01", "2030-05-15", 8, 200),
    (4, "2030-05-01", "2030-05-15", 9, 200),
    (4, "2030-05-01", "2030-05-15", 10, 200),
    (4, "2030-05-01", "2030-05-15", 10, 409),
    (4, "2030-05-01", "2030-05-15", 10, 409),
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, booked_rooms, 
                                   authenticated_ac: AsyncClient): 
    response = await authenticated_ac.post("/bookings", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
        })
    
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms