import logging
from fastapi import FastAPI
from app.controllers import favorite_post_user_controller, auth_controller, user_controller, category_controller, post_user_controller, industry_controller, enterprise_controller, media_post_user_controller, curriculum_controller
from app.configs.db.database import get_db, engine, Base
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse
from typing import Final

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    logger.info("Shutting down the application...")

app: Final[FastAPI] = FastAPI(
    lifespan=lifespan, 
    title="Job vacancy in FastAPI", 
    version="1.0.0",
    default_response_class=ORJSONResponse
)

app.include_router(media_post_user_controller.router)
app.include_router(curriculum_controller.router)
app.include_router(enterprise_controller.router)
app.include_router(favorite_post_user_controller.router)
app.include_router(post_user_controller.router)
app.include_router(industry_controller.router)
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(category_controller.router)