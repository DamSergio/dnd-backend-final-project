from datetime import timedelta
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer
from config import CONFIG
from app.models.user import User

ACCESS_EXPIRES = timedelta(days=15)
REFRESH_EXPIRES = timedelta(days=30)

access_security = JwtAccessBearer(
    CONFIG.jwt_secret,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)

refresh_security = JwtRefreshBearer(
    CONFIG.jwt_secret,
    access_expires_delta=ACCESS_EXPIRES,
    refresh_expires_delta=REFRESH_EXPIRES,
)


async def user_from_token(token: str) -> User | None:
    """Return the user associated with a token value."""
    payload = access_security._decode(token)
    return await User.by_email(payload["subject"]["email"])
