from fastapi import Depends, Request

from app.utils.json_response import JSONResponse
from app.models.models_in_db import User
from app.utils.current_user import current_user

from app.constants.http_errors import auth_errors
from app.constants.http_codes import user_codes


async def delete_invitation(req: Request, user: User = Depends(current_user)):
    """Delete invitation from user's invitations list"""
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
        user.invitations = [
            invitation
            for invitation in user.invitations
            if invitation.campaign_id != data["campaign_id"]
        ]
        await user.save()

        return JSONResponse(
            status_code=200,
            content={
                "code": user_codes.INVITATION_DELETED,
                "message": "Invitation deleted successfully",
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
