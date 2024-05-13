from app.utils.json_response import JSONResponse
from app.utils.password import hash_password
from app.utils.jwt import access_security, refresh_security
from app.models.user import LoginUser
from app.models.models_in_db import User
from app.constants.http_errors import auth_errors
from app.constants.http_codes import auth_codes


async def login_user(user: LoginUser):
    """
    Endpoint to handle user login.
    Validates the user's credentials and generates an access token upon successful login.

    Args:
        user (LoginUser): The user's login information.

    Returns:
        JSONResponse: The response containing the login status and user data.
    """
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

    access_token = access_security.create_access_token(user_in_bd.jwt_subject)
    refresh_token = refresh_security.create_refresh_token(user_in_bd.jwt_subject)

    user_in_bd.refresh_token = refresh_token
    await user_in_bd.save()

    return JSONResponse(
        status_code=200,
        content={
            "code": auth_codes.LOGGED_IN,
            "message": "User logged in",
            "data": {
                "id": user_in_bd.id.__str__(),
                "username": user_in_bd.username,
                "email": user_in_bd.email,
                "profilePicture": user_in_bd.profile_picture,
                "rol": user_in_bd.rol,
                "accessToken": access_token,
            },
        },
    )
