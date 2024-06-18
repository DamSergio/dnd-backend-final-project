from fastapi import Depends, Request

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, campaign_errors
from app.constants.http_codes import campaign_codes


async def delete_campaign(req: Request, user: User = Depends(current_user)):
    """Delete a campaign"""
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

        await campaign.delete()

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.CAMPAIGN_DELETED,
                "message": "Campaign deleted successfully",
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