from fastapi import APIRouter

from app.handlers.character.create_character import create_character
from app.handlers.character.get_user_characters import get_user_characters
from app.handlers.character.get_one import get_one


character_router = APIRouter(prefix="/character", tags=["Character"])

character_router.add_api_route("/create", create_character, methods=["POST"])
character_router.add_api_route("/my-characters", get_user_characters, methods=["GET"])
character_router.add_api_route("/{id}", get_one, methods=["GET"])
