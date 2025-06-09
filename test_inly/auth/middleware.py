from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from starlette.middleware.base import RequestResponseEndpoint
from repository.user import UserRepository
from functools import wraps


class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):

        excluded_path = [
            "/api/public/v1/user/",
            "/api/public/v1/user/auth",
            "/user/registration/",
            "/docs",
            "/docs#",
            "/openapi.json",
            "/docs",
            "/api/public/v1/logout"
        ]

        if request.url.path in excluded_path:
            return await call_next(request)

        token = request.cookies.get("user_cookie")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        # Небольшой костыль так как не JWT auth, поэтому берем пользователя по токену
        user = await UserRepository().get_user(token=token)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        request.state.user = user

        if request.state.user.is_banned:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await call_next(request)



def srv_auth():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs['request']
            if not request.state.user.is_admin:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

            return await func(*args, **kwargs)

        return wrapper

    return decorator