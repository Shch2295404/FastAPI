from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserOut

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    
    """ Регистрация пользователя. """

    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    
    """ Аутентификация пользователя. """

    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="booking_access_token", value=access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    
    """ Удаление куки с токеном при выходе пользователя. """

    response.delete_cookie(key="booking_access_token")
    return {"detail": "User logged out successfully"}


@router.get("/me", response_model=SUserOut)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    
    """ Возвращает данные о текущем авторизованном пользователе. """

    return current_user