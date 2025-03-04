from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        print(user.role.name)
        # Если пользователь найден и его роль соответствует ADMIN или DEVELOPER,
        # создаем токен и сохраняем его в сессии.
        if user and user.role.name in ("ADMIN", "DEVELOPER"):
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token)
        # Допускаем доступ только, если роль пользователя - ADMIN или DEVELOPER.
        if not user or user.role.name not in ("ADMIN", "DEVELOPER"):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key="...")
