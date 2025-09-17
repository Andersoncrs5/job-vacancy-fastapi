import logging
from fastapi import FastAPI
from app.controllers import auth_controller
from app.configs.db.database import get_db, engine, Base
from contextlib import asynccontextmanager
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
    version="1.0.0"
    )

app.include_router(auth_controller.router)