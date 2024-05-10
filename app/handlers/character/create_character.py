from fastapi import Depends
from beanie import Link

from app.utils.json_response import JSONResponse
from app.models.character import CreateCharacter, Character
from app.models.user import User
from app.middleware.protected import protected_route

from app.constants.http_errors import auth_errors, character_errors
from app.constants.http_codes import character_codes


async def create_character(
    character_data: CreateCharacter, user: User = Depends(protected_route)
):
    """
    Endpoint to handle character creation.
    Creates a new character with the provided information.

    Returns:
        JSONResponse: The response containing the character creation status.
    """
    if not user:
        return JSONResponse(
            status_code=400,
            content={
                "error": auth_errors.INVALID_TOKEN,
                "message": "Invalid token provided",
            },
        )

    if not validate_character_data(character_data):
        return JSONResponse(
            status_code=400,
            content={
                "error": character_errors.INVALID_CHARACTER_DATA,
                "message": "Invalid character data provided",
            },
        )

    await create_character_in_db(character_data, user)

    return JSONResponse(
        status_code=200,
        content={
            "code": character_codes.CHARACTER_CREATED,
            "message": "Character created successfully",
        },
    )


async def create_character_in_db(character_data: CreateCharacter, user: User):
    new_character: Character = Character(
        name=character_data.name,
        gender=character_data.gender,
        age=character_data.age,
        background=character_data.background,
        alignment=character_data.alignment,
        personality_traits=character_data.personality_traits,
        ideals=character_data.ideals,
        bonds=character_data.bonds,
        flaws=character_data.flaws,
        history=character_data.history,
        character_race=character_data.character_race,
        character_class=character_data.character_class,
        hit_points=character_data.hit_points,
        armor_class=character_data.armor_class,
        speed=character_data.speed,
        saving_throws=character_data.saving_throws,
        armor_proficiencies=character_data.armor_proficiencies,
        weapon_proficiencies=character_data.weapon_proficiencies,
        tool_proficiencies=character_data.tool_proficiencies,
        stats=character_data.stats,
        coins=character_data.coins,
        skills=character_data.skills,
        traits=character_data.traits,
        items=character_data.items,
        languages=character_data.languages,
    )

    await new_character.insert()

    character_link = Link(new_character, document_class=Character)
    user.characters.append(character_link)

    await user.save()


def validate_character_data(character_data: CreateCharacter):
    if not character_data:
        return False

    if (
        not character_data.name
        or not character_data.gender
        or not character_data.age
        or not character_data.alignment
        or not character_data.background
        or not character_data.character_class
        or not character_data.character_race
        or not character_data.hit_points
        or not character_data.speed
        or not character_data.saving_throws
        or not character_data.stats
        or not character_data.coins
        or not character_data.skills
        or not character_data.traits
        or not character_data.items
        or not character_data.languages
    ):
        return False

    return True
