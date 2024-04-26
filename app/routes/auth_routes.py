from fastapi import APIRouter
from app.models.user import RegisterUser, LoginUser

from app.handlers.auth.register import register_user
from app.handlers.auth.login import login_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

auth_router.add_api_route("/register", register_user, methods=["POST"])
auth_router.add_api_route("/login", login_user, methods=["POST"])
