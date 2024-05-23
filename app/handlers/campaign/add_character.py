from fastapi import Depends, Request
from beanie import Link, WriteRules

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User, Campaign, Character
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors, campaign_errors, character_errors
from app.constants.http_codes import campaign_codes


async def add_character_to_campaign(req: Request, user: User = Depends(current_user)):
    """Add character to campaign"""
    try:
        if not user:
            return JSONResponse(
                status_code=400,
                content={
                    "error": auth_errors.INVALID_TOKEN,
                    "message": "Invalid token provided",
                },
            )

        data = await req.json()
        campaign_id = data.get("campaign_id")
        character_id = data.get("character_id")

        campaign = await Campaign.get(campaign_id)
        if not campaign:
            return JSONResponse(
                status_code=404,
                content={
                    "error": campaign_errors.CAMPAIGN_NOT_FOUND,
                    "message": "Campaign not found",
                },
            )

        character = await Character.get(character_id)
        if not character:
            return JSONResponse(
                status_code=404,
                content={
                    "error": character_errors.NO_CHARACTER_FOUND,
                    "message": "Character not found",
                },
            )

        character_link = Link(character, document_class=Character).to_ref()
        campaign.players.append(character_link)
        await campaign.save(link_rule=WriteRules.WRITE)

        return JSONResponse(
            status_code=200,
            content={
                "code": campaign_codes.CHARACTER_ADDED,
                "message": "Character added successfully",
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
