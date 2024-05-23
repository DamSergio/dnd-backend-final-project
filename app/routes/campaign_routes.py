from fastapi import APIRouter

from app.handlers.campaign.create_campaign import create_campaign
from app.handlers.campaign.get_user_campaigns import get_user_campaigns
from app.handlers.campaign.get_one import get_one
from app.handlers.campaign.edit_notes import edit_notes
from app.handlers.campaign.delete_campaign import delete_campaign

from app.handlers.campaign.add_character import add_character_to_campaign
from app.handlers.campaign.invite_player import invite_player
from app.handlers.campaign.roll_dice import roll_dice


campaign_router = APIRouter(prefix="/campaign", tags=["Campaigns"])

campaign_router.add_api_route("/create", create_campaign, methods=["POST"])
campaign_router.add_api_route("/my-campaigns", get_user_campaigns, methods=["GET"])
campaign_router.add_api_route("/{id}", get_one, methods=["GET"])
campaign_router.add_api_route("/{id}/notes", edit_notes, methods=["PATCH"])
campaign_router.add_api_route("/{id}/delete", delete_campaign, methods=["DELETE"])

campaign_router.add_api_route(
    "/add-character", add_character_to_campaign, methods=["POST"]
)
campaign_router.add_api_route("/invite", invite_player, methods=["PATCH"])
campaign_router.add_api_route("/roll", roll_dice, methods=["PATCH"])
