from fastapi import Depends
from beanie import Link, WriteRules

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign
from app.models.campaign import CreateCampaign
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors
from app.constants.http_errors import campaign_errors
from app.constants.http_codes import campaign_codes


async def create_campaign(campaign: CreateCampaign, user: User = Depends(current_user)):
    """
    Create a new campaign.

    Args:
        campaign (CreateCampaign): The campaign data to be created.
        user (User, optional): User that create the campaign.

    Returns:
        JSONResponse: The response containing the status code and message.

    Raises:
        JSONResponse: If the user is not authenticated or the campaign data is invalid.
    """
    try:
        if not user:
            return JSONResponse(
                status_code=400,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token provided",
                },
            )

        if not validate_campaign(campaign):
            return JSONResponse(
                status_code=400,
                content={
                    "error": campaign_errors.INVALID_CAMPAIGN_DATA,
                    "message": "Invalid data",
                },
            )

        await create_campaign_in_db(campaign, user)

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.CAMPAIGN_CREATED,
                "message": "Campaign created successfully",
            },
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL SERVER ERROR",
                "message": "Failed to create campaign",
            },
        )


async def create_campaign_in_db(campaign: CreateCampaign, user: User):
    user_link = Link(user, document_class=User)
    new_campaign: Campaign = Campaign(
        name=campaign.name,
        description=campaign.description,
        notes=campaign.notes,
        dungeon_master=user_link.to_ref(),
    )

    await new_campaign.insert(link_rule=WriteRules.WRITE)


def validate_campaign(campaign: CreateCampaign):
    if not campaign.name or not campaign.description:
        return False

    return True
