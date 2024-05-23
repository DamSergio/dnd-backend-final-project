from fastapi import APIRouter

from app.handlers.campaign.create_campaign import create_campaign
from app.handlers.campaign.get_user_campaigns import get_user_campaigns
from app.handlers.campaign.get_one import get_one

from app.handlers.campaign.add_character import add_character_to_campaign
from app.handlers.campaign.invite_player import invite_player


campaign_router = APIRouter(prefix="/campaign", tags=["Campaigns"])

campaign_router.add_api_route("/create", create_campaign, methods=["POST"])
campaign_router.add_api_route("/my-campaigns", get_user_campaigns, methods=["GET"])
campaign_router.add_api_route("/{id}", get_one, methods=["GET"])

campaign_router.add_api_route(
    "/add-character", add_character_to_campaign, methods=["POST"]
)
campaign_router.add_api_route("/invite", invite_player, methods=["PATCH"])
