from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from auth.middleware import AuthMiddleWare
from db_helper import init_db, close_db
import settings
from settings import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    from api.public import router as api_v1_router
    from api.srv import router as api_srv_router

    await init_db()
    logger.info("Init db success")
    app.include_router(api_v1_router)
    app.include_router(api_srv_router)

    yield

    await close_db()
    logger.info("Close db success")


app = FastAPI(lifespan=lifespan)
app.add_middleware(AuthMiddleWare)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
