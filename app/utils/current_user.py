from fastapi import Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.models.models_in_db import User
from app.utils.jwt import access_security, user_from_credentials


async def current_user(
    auth: JwtAuthorizationCredentials = Security(access_security),
) -> User | None:
    """Return the current authorized user."""
    if not auth:
        return None

    return await user_from_credentials(auth)
