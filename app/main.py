from fastapi import FastAPI
from app.routes.auth_routes import auth_router
from app.routes.user_routes import user_router
from app.routes.character_routes import character_router
from starlette.middleware.cors import CORSMiddleware

from app.utils.db_connection import connect_to_mongo

import firebase

config = {
    "apiKey": "AIzaSyDZcAsUGY6dFE-jZvdUUqFxZ9QyFQpAStw",
    "authDomain": "dnd-app-1656b.firebaseapp.com",
    "databaseURL": "https://dnd-app-1656b-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "dnd-app-1656b",
    "storageBucket": "dnd-app-1656b.appspot.com",
    "messagingSenderId": "937003611950",
    "appId": "1:937003611950:web:40d517aaf815fb5f22ecbf",
    "measurementId": "G-9D2288S89Z",
}

firebase_app = firebase.initialize_app(config)
storage = firebase_app.storage()

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


@app.get("/")
def read_root():
    return {"message": "Hello World"}
