from fastapi import UploadFile, Request, Depends

from app.utils.json_response import JSONResponse
from app.models.models_in_db import Character, User
from app.utils.firebase_storage import storage
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, character_errors
from app.constants.http_codes import character_codes


async def edit_picture(req: Request, user: User = Depends(current_user)):
    """Edit a character's picture."""
    if not user:
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.INVALID_TOKEN,
                "message": "Invalid token",
            },
        )

    character = await Character.get(req.path_params["id"])
    if not character:
        return JSONResponse(
            status_code=404,
            content={
                "error": character_errors.NO_CHARACTER_FOUND,
                "message": "No character found",
            },
        )

    form = await req.form()
    if "picture" not in form:
        return JSONResponse(
            status_code=400,
            content={
                "error": character_errors.INVALID_CHARACTER_DATA,
                "message": "Invalid character data",
            },
        )

    picture: UploadFile = form["picture"]

    try:
        # Upload the file to firebase
        storage.child(f"characters/{character.id}").put(picture.file)
        pic_url = storage.child(f"characters/{character.id}").get_url()
        character.picture = pic_url
        await character.save()
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
            "code": character_codes.CHARACTER_UPDATED,
            "message": "Character updated",
            "data": {
                "picture": pic_url,
            },
        },
    )
