from fastapi import Depends, Request

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, campaign_errors
from app.constants.http_codes import campaign_codes

from app.socket.socket import sio


async def invite_player(req: Request, user: User = Depends(current_user)):
    """"""
    try:
        if not user:
            return JSONResponse(
                status_code=401,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token",
                },
            )

        data = await req.json()
        campaign_id = data["campaign_id"]
        player_email = data["player_email"]

        campaign = await Campaign.get(campaign_id, fetch_links=True, nesting_depth=2)
        if not campaign:
            return JSONResponse(
                status_code=404,
                content={
                    "error": campaign_errors.CAMPAIGN_NOT_FOUND,
                    "message": "No campaign found",
                },
            )

        if campaign.dungeon_master.email != user.email:
            return JSONResponse(
                status_code=403,
                content={
                    "error": campaign_errors.UNAUTHORIZED,
                    "message": "You are not authorized to invite players to this campaign",
                },
            )

        player = await User.find_one({"email": player_email})
        if not player:
            return JSONResponse(
                status_code=404,
                content={
                    "error": auth_errors.USER_NOT_FOUND,
                    "message": "No user found with the provided email",
                },
            )

        if player.id in [player.user.id for player in campaign.players]:
            return JSONResponse(
                status_code=400,
                content={
                    "error": campaign_errors.PLAYER_ALREADY_INVITED,
                    "message": "Player is already invited to this campaign",
                },
            )

        if campaign.name in [
            invitation.campaign_name for invitation in player.invitations
        ]:
            return JSONResponse(
                status_code=400,
                content={
                    "error": campaign_errors.PLAYER_ALREADY_INVITED,
                    "message": "Player is already invited to this campaign",
                },
            )

        player.invitations.append(
            {
                "campaign_id": campaign_id,
                "campaign_name": campaign.name,
                "dungeon_master": user.username,
            }
        )
        await player.save()

        if player.socket_id:
            await sio.emit(
                event="new_invitation",
                data={
                    "campaign_id": campaign_id,
                    "campaign_name": campaign.name,
                    "dungeon_master": user.username,
                },
                to=player.socket_id,
            )

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.PLAYER_INVITED,
                "message": "Player invited successfully",
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
