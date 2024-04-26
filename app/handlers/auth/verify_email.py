from app.utils.jwt import user_from_token
from app.utils.json_response import JSONResponse
from app.constants.http_errors import auth_errors
from app.constants.http_codes import auth_codes
from app.models.user import User


async def verify_email(token: str):
    user: User = await user_from_token(token)
    if not user:
        return JSONResponse(
            status_code=404,
            content={"error": auth_errors.INVALID_TOKEN, "message": "Invalid token"},
        )

    user.verfied = True
    await user.save()

    return JSONResponse(
        status_code=200,
        content={"code": auth_codes.EMAIL_VERIFIED, "message": "Email verified"},
    )
