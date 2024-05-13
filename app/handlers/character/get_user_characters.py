from fastapi import Depends

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors
from app.constants.http_codes import character_codes


async def get_user_characters(user: User = Depends(current_user)):
    """
    Endpoint to handle character retrieval.
    Retrieves all characters associated with the user.

    Returns:
        JSONResponse: The response containing the user's characters.
    """
    if not user:
        return JSONResponse(
            status_code=400,
            content={
                "error": auth_errors.INVALID_TOKEN,
                "message": "Invalid token provided",
            },
        )

    characters = []
    for character_ref in user.characters:
        character = await character_ref.fetch()
        character_data = character.model_dump()
        character_data["user"] = user.id.__str__()
        characters.append(character_data)

    return JSONResponse(
        status_code=200,
        content={
            "code": character_codes.CHARACTERS_RETRIEVED,
            "message": "Characters retrieved",
            "data": characters,
        },
    )
