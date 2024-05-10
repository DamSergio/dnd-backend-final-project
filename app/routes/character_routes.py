from fastapi import APIRouter

from app.handlers.character.create_character import create_character


character_router = APIRouter(prefix="/character", tags=["Character"])

character_router.add_api_route("/create", create_character, methods=["POST"])
