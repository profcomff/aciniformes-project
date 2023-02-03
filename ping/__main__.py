from .asgi import ping_app
import uvicorn


if __name__ == "__main__":
    uvicorn.run(ping_app)