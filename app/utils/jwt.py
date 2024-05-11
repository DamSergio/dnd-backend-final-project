from datetime import timedelta
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer
from config import CONFIG
from app.models.models_in_db import User

ACCESS_EXPIRES = timedelta(days=30)

EMAIL_CONFIRMATION_EXPIRES = timedelta(days=1)

access_security = JwtAccessBearer(
    CONFIG.jwt_secret,
    access_expires_delta=ACCESS_EXPIRES,
)

email_access_security = JwtAccessBearer(
    CONFIG.jwt_secret, access_expires_delta=EMAIL_CONFIRMATION_EXPIRES
)


async def user_from_token(token: str) -> User | None:
    """Return the user associated with a token value."""
    try:
        payload = access_security._decode(token)
        return await User.by_email(payload["subject"]["email"])
    except Exception:
        return None
