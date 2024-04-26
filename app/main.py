from fastapi import FastAPI, Request, Depends
from app.routes.auth_routes import auth_router
from app.routes.user_routes import user_router

from app.utils.db_connection import connect_to_mongo

app = FastAPI(
    title="dnd-api",
    description="An API for Dungeons and Dragons",
    version="0.1.0",
    lifespan=connect_to_mongo,
)

app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
