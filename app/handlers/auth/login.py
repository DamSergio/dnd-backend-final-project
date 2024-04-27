from app.utils.json_response import JSONResponse
from app.utils.password import hash_password
from app.utils.jwt import access_security
from app.models.user import LoginUser, User
from app.constants.http_errors import auth_errors
from app.constants.http_codes import auth_codes


async def login_user(user: LoginUser):
    user_in_bd = await User.by_email(user.email)
    if not user_in_bd:
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.INCORRECT_CREDENTIALS,
                "message": "Invalid email or password",
            },
        )

    hashed_password = hash_password(user.password)
    if user_in_bd.password != hashed_password:
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.INCORRECT_CREDENTIALS,
                "message": "Invalid email or password",
            },
        )

    if not user_in_bd.verfied:
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.NOT_VERIFIED,
                "message": "User is not yet verified",
            },
        )

    token = access_security.create_access_token(user_in_bd.jwt_subject)

    return JSONResponse(
        status_code=200,
        content={
            "code": auth_codes.LOGGED_IN,
            "message": "User logged in",
            "data": {
                "username": user_in_bd.username,
                "email": user_in_bd.email,
                "profilePicture": user_in_bd.profile_picture,
                "token": token,
            },
        },
    )
