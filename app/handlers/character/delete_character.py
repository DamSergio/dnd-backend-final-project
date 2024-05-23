from fastapi import Request, Depends
from beanie import Link

from app.utils.json_response import JSONResponse
from app.models.models_in_db import Character, User
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, character_errors
from app.constants.http_codes import character_codes


async def delete_character(req: Request, user: User = Depends(current_user)):
    """"""
    if not user:
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.INVALID_TOKEN,
                "message": "Invalid token",
            },
        )

    id = req.path_params["id"]
    character = await Character.get(id, fetch_links=True)
    if not character:
        return JSONResponse(
            status_code=404,
            content={
                "error": character_errors.NO_CHARACTER_FOUND,
                "message": "No character found",
            },
        )

    character_user: User = character.user
    if character_user.id != user.id and user.rol != "admin":
        return JSONResponse(
            status_code=401,
            content={
                "error": auth_errors.NOT_ENOUGHT_PERMISSIONS,
                "message": "No tienes permisos",
            },
        )

    character_link = None
    for link in user.characters:
        char: Character = await link.fetch()
        if char.id == character.id:
            character_link = link
            break

    if character_link is None:
        return JSONResponse(
            status_code=400,
            content={
                "error": character_errors.NO_CHARACTER_FOUND,
                "message": "Character link not found in user's characters list",
            },
        )

    user.characters.remove(link)
    await user.save()
    await character.delete()

    return JSONResponse(
        status_code=200,
        content={
            "code": character_codes.CHARACTER_DELETED,
            "message": "Character deleted",
        },
    )
