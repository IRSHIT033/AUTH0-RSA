import uvicorn
from fastapi import FastAPI
import fastapi
from hopprai.core.config import settings
from hopprai.api.v1.endpoints.auth import router as auth_router


def initialize_backend_application() -> fastapi.FastAPI:
    app = FastAPI()
    app.include_router(auth_router)
    return app


backend_app: fastapi.FastAPI = initialize_backend_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:backend_app",
        host=settings.SERVER_HOST,
        workers=settings.SERVER_WORKERS,
        reload=settings.SERVER_RELOAD,
        port=settings.SERVER_PORT,
        log_level=settings.LOG_LEVEL,
    )
