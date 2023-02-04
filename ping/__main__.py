from .api.asgi import ping_app
import uvicorn


if __name__ == "__main__":
    uvicorn.run(ping_app, port=8001)
