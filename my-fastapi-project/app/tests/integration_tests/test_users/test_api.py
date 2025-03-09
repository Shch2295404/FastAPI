import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email,password,status_code", [
    ("kot@pes.com", "kotopes", 200),  # Пользователь успешно зарегистрирован
    ("kot@pes.com", "kot0pes", 409),  # Пользователь уже существует
    ("pes@kot.com", "pesokot", 200),  # Пользователь успешно зарегистрирован
    ("abcdef", "kotopes", 422)        # Невалидная электронная почта    
    ])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
        })
    
    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),                 # Пользователь успешно аутентифицирован
    ("artem@example.com", "artem", 200),            # Пользователь успешно аутентифицирован
    ("nonexistent@example.com", "password", 401),   # Пользователь не существует
    ("test@test.com", "wrongpassword", 401),        # Неверный пароль    
    ])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
        })
    
    assert response.status_code == status_code
