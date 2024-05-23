import socketio

from app.models.models_in_db import User


sio = socketio.AsyncServer(
    cors_allowed_origins=[], methods=["GET", "POST"], async_mode="asgi"
)
socket_app = socketio.ASGIApp(sio)


@sio.on("connect")
async def connect(sid, environ):
    user_id: str = environ["QUERY_STRING"].split("=")[1].split("&")[0]
    user = await User.get(user_id)
    user.socket_id = sid
    await user.save()


@sio.on("disconnect")
async def disconnect(sid):
    user = await User.by_socket_id(sid)
    if not user:
        return

    user.socket_id = ""
    await user.save()
