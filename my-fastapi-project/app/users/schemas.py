from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr


# Определяем перечисление для ролей на уровне Pydantic
class UserRoleEnum(str, Enum):
    USER = "Пользователь"
    DEVELOPER = "Разработчик"
    ADMIN = "Администратор"

# Схема для авторизации (например, логин)
class SUserAuth(BaseModel):
    email: EmailStr
    password: str

# Схема для регистрации или отображения данных пользователя
class SUserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRoleEnum

    model_config = ConfigDict(from_attributes=True)
