from fastapi import APIRouter
from app.handlers.auth.register import register_user
from app.handlers.auth.verify_email import verify_email
from app.handlers.auth.login import login_user
from app.handlers.auth.refresh import refresh

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

auth_router.add_api_route("/register", register_user, methods=["POST"])
auth_router.add_api_route("/verify/{token}", verify_email, methods=["GET"])
auth_router.add_api_route("/login", login_user, methods=["POST"])
auth_router.add_api_route("/refresh", refresh, methods=["GET"])
