from fastapi import Depends, Request

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, campaign_errors
from app.constants.http_codes import campaign_codes


async def edit_notes(req: Request, user: User = Depends(current_user)):
    """Edit campaign notes"""
    try:
        if not user:
            return JSONResponse(
                status_code=400,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token provided",
                },
            )

        id = req.path_params.get("id")
        campaign = await Campaign.get(id)
        if not campaign:
            return JSONResponse(
                status_code=404,
                content={
                    "error": campaign_errors.CAMPAIGN_NOT_FOUND,
                    "message": "Campaign not found",
                },
            )

        data = await req.json()
        notes = data["notes"]
        campaign.notes = notes
        await campaign.save()

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.CAMPAIGN_UPDATED,
                "message": "Campaign notes updated successfully",
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
