from app.utils.json_response import JSONResponse
from app.utils.password import hash_password
from app.models.user import RegisterUser, User
from app.constants.http_errors import auth_errors
from app.constants.http_codes import auth_codes


async def register_user(user: RegisterUser):
    if user.password != user.confirm_password:
        return JSONResponse(
            status_code=400,
            content={
                "error": auth_errors.PASSWORDS_DO_NOT_MATCH,
                "message": "Passwords do not match",
            },
        )

    user_exists = await User.by_email(user.email)
    if user_exists:
        return JSONResponse(
            status_code=409,
            content={
                "error": auth_errors.EMAIL_ALREADY_IN_USE,
                "message": "Email already in use",
            },
        )

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        profile_picture=f"https://avatar.iran.liara.run/public/boy?username={user.username}",
    )
    await new_user.insert()

    # TODO: Send email verification

    return JSONResponse(
        status_code=201,
        content={
            "code": auth_codes.USER_CREATED,
            "message": "User created",
        },
    )
