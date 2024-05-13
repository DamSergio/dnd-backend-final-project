from fastapi import Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.utils.json_response import JSONResponse
from app.utils.jwt import access_security, refresh_security, user_from_credentials
from app.models.models_in_db import User

from app.constants.http_errors import auth_errors
from app.constants.http_codes import auth_codes


async def refresh(
    auth: JwtAuthorizationCredentials = Security(access_security),
) -> JSONResponse:
    """Return a new access token from an access token."""
    if not auth:
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.INVALID_TOKEN,
                "message": "Invalid token provided",
            },
        )

    user = await user_from_credentials(auth)
    refresh_security._decode(
        user.refresh_token
    )  # Si el decode falla salta un error 401

    access_token = access_security.create_access_token(subject=auth.subject)
    return JSONResponse(
        status_code=200,
        content={
            "code": auth_codes.TOKEN_REFRESHED,
            "message": "Access token refreshed",
            "data": {"accessToken": access_token},
        },
    )
