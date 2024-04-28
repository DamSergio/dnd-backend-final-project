from app.utils.json_response import JSONResponse
from app.utils.password import hash_password
from app.models.user import RegisterUser, User
from app.constants.http_errors import auth_errors
from app.constants.http_codes import auth_codes
from app.utils.mailer import send_email


async def register_user(user: RegisterUser):
    """
    Register a new user.

    This endpoint is used to register a new user in the system. It performs the following steps:
    1. Checks if the password and confirm_password fields match.
    2. Checks if the user's email is already in use.
    3. Hashes the user's password.
    4. Creates a new User object with the provided information.
    5. Inserts the new user into the database.
    6. Sends a confirmation email to the new user.
    7. Returns a JSON response with the status code and a message indicating the success of the registration.

    Args:
        user (RegisterUser): The user object containing the registration information.

    Returns:
        JSONResponse: A JSON response with the status code and a message indicating the success of the registration.
    """
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

    await send_email(new_user)

    return JSONResponse(
        status_code=201,
        content={
            "code": auth_codes.USER_CREATED,
            "message": "User created",
        },
    )
