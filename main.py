import uvicorn
from config import CONFIG


if __name__ == "__main__":
    uvicorn.run(
        CONFIG.uvicorn_app, host=CONFIG.host, port=CONFIG.port, reload=CONFIG.reload
    )
