from fastapi import Depends

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors
from app.constants.http_codes import campaign_codes


async def get_user_campaigns(user: User = Depends(current_user)):
    """User campaigns"""
    try:
        if not user:
            return JSONResponse(
                status_code=400,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token provided",
                },
            )

        # Campañas en las que el usuario es DM
        campaigns = []
        campaigns = await Campaign.find(
            Campaign.dungeon_master.email == user.email,
            fetch_links=True,
            nesting_depth=1,
        ).to_list()

        # Campañas en las que el usuario es jugador
        user_characters = await User.get(user.id, fetch_links=True, nesting_depth=2)
        for character in user_characters.characters:
            for campaign in character.campaigns:
                campaign_db = await Campaign.get(
                    campaign.id, fetch_links=True, nesting_depth=1
                )
                campaigns.append(campaign_db)

        campaigns_dict = []
        for campaign in campaigns:
            campaign_data = campaign.model_dump(exclude=["dungeon_master", "players"])
            campaign_data["dungeon_master"] = campaign.dungeon_master.email
            campaigns_dict.append(campaign_data)

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.CAMPAIGNS_RETRIEVED,
                "message": "Campaigns retrieved",
                "data": campaigns_dict,
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL SERVER ERROR",
                "message": "Internal server error occurred. Please try again later.",
            },
        )
