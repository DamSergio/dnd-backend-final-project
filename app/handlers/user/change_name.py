from fastapi import Request, Depends

from app.utils.json_response import JSONResponse
from app.utils.current_user import current_user
from app.models.models_in_db import User

from app.constants.http_errors import auth_errors
from app.constants.http_codes import user_codes


async def change_name(req: Request, user: User = Depends(current_user)):
    """Change the user's name."""
    try:
        if not user:
            return JSONResponse(
                status_code=401,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token",
                },
            )

        data = await req.json()
        if "username" not in data:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "INVALID_DATA",
                    "message": "Invalid data",
                },
            )

        user.username = data["username"]
        await user.save()

        return JSONResponse(
            status_code=200,
            content={
                "code": user_codes.USER_UPDATED,
                "message": "Name updated successfully.",
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error. Failed to change the name.",
            },
        )
