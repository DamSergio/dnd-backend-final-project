from fastapi import Request
from app.models.user import User
from app.utils.jwt import user_from_token


async def protected_route(request: Request) -> User | None:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    if not auth_header.startswith("Bearer"):
        return None

    token = auth_header.split(" ")[1]
    return await user_from_token(token)
