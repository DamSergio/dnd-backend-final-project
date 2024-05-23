from fastapi import Request, Depends

from app.utils.json_response import JSONResponse
from app.utils.current_user import current_user
from app.models.models_in_db import User, Character

from app.constants.http_errors import auth_errors, character_errors
from app.constants.http_codes import character_codes


async def edit_stats(req: Request, user: User = Depends(current_user)):
    """Edit the stats of a character."""
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
                "message": "Character not found.",
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

    data = await req.json()
    if (
        "str" not in data
        or "dex" not in data
        or "con" not in data
        or "int" not in data
        or "wis" not in data
        or "cha" not in data
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": character_errors.INVALID_CHARACTER_DATA,
                "message": "Invalid character data",
            },
        )

    character.stats.str = data["str"]
    character.stats.dex = data["dex"]
    character.stats.con = data["con"]
    character.stats.int = data["int"]
    character.stats.wis = data["wis"]
    character.stats.cha = data["cha"]
    await character.save()

    return JSONResponse(
        status_code=200,
        content={
            "code": character_codes.CHARACTER_UPDATED,
            "message": "Character updated",
        },
    )
