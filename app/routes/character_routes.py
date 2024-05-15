from fastapi import APIRouter

from app.handlers.character.create_character import create_character
from app.handlers.character.get_user_characters import get_user_characters
from app.handlers.character.get_one import get_one

from app.handlers.character.edit_picture import edit_picture
from app.handlers.character.edit_languages import edit_languages
from app.handlers.character.edit_characteristics import edit_characteristics
from app.handlers.character.edit_stats import edit_stats
from app.handlers.character.edit_personality import edit_personality


character_router = APIRouter(prefix="/character", tags=["Character"])

character_router.add_api_route("/create", create_character, methods=["POST"])
character_router.add_api_route("/my-characters", get_user_characters, methods=["GET"])
character_router.add_api_route("/{id}", get_one, methods=["GET"])

# Edit character routes
character_router.add_api_route("/{id}/picture", edit_picture, methods=["PATCH"])
character_router.add_api_route("/{id}/languages", edit_languages, methods=["PATCH"])
character_router.add_api_route(
    "/{id}/characteristics", edit_characteristics, methods=["PATCH"]
)
character_router.add_api_route("/{id}/stats", edit_stats, methods=["PATCH"])
character_router.add_api_route("/{id}/personality", edit_personality, methods=["PATCH"])
