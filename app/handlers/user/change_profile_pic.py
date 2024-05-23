from fastapi import UploadFile, Request, Depends

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User
from app.utils.firebase_storage import storage
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors
from app.constants.http_codes import user_codes


async def change_profile_pic(req: Request, user: User = Depends(current_user)):
    """Change the user's profile picture."""
    try:
        if not user:
            return JSONResponse(
                status_code=401,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token",
                },
            )

        form = await req.form()
        if "picture" not in form:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "INVALID_DATA",
                    "message": "Invalid data",
                },
            )

        picture: UploadFile = form["picture"]
        try:
            # Upload the file to firebase
            storage.child(f"users/{user.id}").put(picture.file)
            pic_url = storage.child(f"users/{user.id}").get_url()
            user.profile_picture = pic_url
            await user.save()
        except Exception:
            return JSONResponse(
                status_code=500,
                content={
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": "Internal server error. Failed to upload the picture.",
                },
            )

        return JSONResponse(
            status_code=200,
            content={
                "code": user_codes.USER_UPDATED,
                "message": "Profile picture updated successfully.",
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL SERVER ERROR",
                "message": "Internal server error occurred. Please try again later.",
            },
        )
