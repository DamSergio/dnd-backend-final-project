from fastapi import Depends

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, campaign_errors
from app.constants.http_codes import campaign_codes


async def get_one(id: str, user: User = Depends(current_user)):
    try:
        if not user:
            return JSONResponse(
                status_code=401,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token",
                },
            )

        try:
            campaign = await Campaign.get(id, fetch_links=True, nesting_depth=2)
        except:
            campaign = None

        if not campaign:
            return JSONResponse(
                status_code=404,
                content={
                    "error": campaign_errors.CAMPAIGN_NOT_FOUND,
                    "message": "No campaign found",
                },
            )

        campaign_data = campaign.model_dump(exclude=["dungeon_master", "players"])
        campaign_data["dungeon_master"] = campaign.dungeon_master.email
        campaign_data["players"] = []
        for player in campaign.players:
            player_data = player.model_dump(exclude=["campaigns", "user"])
            player_data["user"] = player.user.id.__str__()
            campaign_data["players"].append(player_data)

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.CAMPAIGN_RETRIEVED,
                "message": "Campaign retrieved successfully",
                "data": campaign_data,
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
