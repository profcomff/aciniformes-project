import uvicorn

from .api.asgi import ping_app

if __name__ == "__main__":
    uvicorn.run(ping_app, port=8001)
