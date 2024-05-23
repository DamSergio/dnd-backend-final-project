from fastapi import Depends, Request

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, campaign_errors
from app.constants.http_codes import campaign_codes

from app.socket.socket import sio


async def roll_dice(req: Request, user: User = Depends(current_user)):
    """Roll dice for a campaign"""
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
        if "campaign_id" not in data or "dice" not in data or "result" not in data:
            return JSONResponse(
                status_code=400,
                content={
                    "error": campaign_errors.INVALID_ROLL_DATA,
                    "message": "Missing required data",
                },
            )

        campaign = await Campaign.get(
            data["campaign_id"], fetch_links=True, nesting_depth=2
        )
        if not campaign:
            return JSONResponse(
                status_code=404,
                content={
                    "error": campaign_errors.CAMPAIGN_NOT_FOUND,
                    "message": "Campaign not found",
                },
            )

        campaign.rolls.append(
            {
                "dice": data["dice"],
                "result": data["result"],
                "user_id": user.id.__str__(),
                "username": user.username,
                "profile_picture": user.profile_picture,
            }
        )
        await campaign.save()

        sockets = []
        sockets.append(campaign.dungeon_master.socket_id)
        for player in campaign.players:
            if player.user.socket_id:
                sockets.append(player.user.socket_id)

        if sockets:
            await sio.emit(
                event="roll_added",
                data={
                    "dice": data["dice"],
                    "result": data["result"],
                    "user_id": user.id.__str__(),
                    "username": user.username,
                    "profile_picture": user.profile_picture,
                },
                to=sockets,
            )

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.ROLL_SUCCESSFUL,
                "message": "Dice rolled successfully",
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Internal server error occurred. Please try again later.",
            },
        )
