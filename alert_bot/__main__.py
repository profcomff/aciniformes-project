import uvicorn

from .asgi import app

if __name__ == "__main__":
    uvicorn.run(app, port=8002)
