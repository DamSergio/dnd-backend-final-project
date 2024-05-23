from fastapi import APIRouter

from app.handlers.user.delete_invitation import delete_invitation


user_router = APIRouter(prefix="/user", tags=["User"])

user_router.add_api_route("/delete-invitation", delete_invitation, methods=["PATCH"])
