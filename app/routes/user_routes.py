from fastapi import APIRouter

from app.handlers.user.delete_invitation import delete_invitation
from app.handlers.user.change_profile_pic import change_profile_pic
from app.handlers.user.change_name import change_name


user_router = APIRouter(prefix="/user", tags=["User"])

user_router.add_api_route("/delete-invitation", delete_invitation, methods=["PATCH"])
user_router.add_api_route("/picture", change_profile_pic, methods=["PATCH"])
user_router.add_api_route("/name", change_name, methods=["PATCH"])
