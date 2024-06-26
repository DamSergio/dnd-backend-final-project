from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.auth_routes import auth_router
from app.routes.user_routes import user_router
from app.routes.character_routes import character_router
from app.routes.campaign_routes import campaign_router
from app.socket.socket import socket_app

from app.utils.db_connection import connect_to_mongo

app = FastAPI(
    title="dnd-api",
    description="An API for Dungeons and Dragons",
    version="0.1.0",
    lifespan=connect_to_mongo,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(character_router)
app.include_router(campaign_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


app.mount("/", socket_app)
