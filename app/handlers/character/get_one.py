from app.utils.json_response import JSONResponse
from app.models.models_in_db import User
from app.models.models_in_db import Character

from app.constants.http_errors import character_errors
from app.constants.http_codes import character_codes


async def get_one(id: str):
    try:
        character = await Character.get(id, fetch_links=True)
    except:
        character = None

    if not character:
        return JSONResponse(
            status_code=404,
            content={
                "error": character_errors.NO_CHARACTER_FOUND,
                "message": "No character found",
            },
        )

    user: User = character.user
    user_id: str = user.id.__str__()

    return JSONResponse(
        status_code=200,
        content={
            "code": character_codes.CHARACTER_RETRIEVED,
            "message": "Character retrieved successfully",
            "data": {
                **character.model_dump(exclude=["user", "campaigns"]),
                "user": user_id,
            },
        },
    )
