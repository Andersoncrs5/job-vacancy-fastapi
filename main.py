from fastapi import FastAPI
from app.controllers import (
    favorite_post_user_controller, auth_controller, user_controller,
    category_controller, post_user_controller, industry_controller,
    enterprise_controller, media_post_user_controller, curriculum_controller,
    skill_controller, my_skill_controller, post_enterprise_controller,
    favorite_post_enterprise_controller, employee_enterprise_controller,
    review_enterprise_controller, saved_search_controller, area_controller,
    vacancy_controller, vacancy_skill_controller, address_user_controller,
    address_enterprise_controller, application_controller, follow_controller,
    follow_enterprise_controller
)
from app.configs.db.database import get_db, engine, Base
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse
from typing import Final
import structlog
import uuid

def setup_logging() -> structlog.BoundLogger:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()

logger: Final[structlog.BoundLogger] = setup_logging()


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
    default_response_class=ORJSONResponse,
    contact={
        "name": "Anderson C. R. da S.",  
        "url": "https://github.com/Andersoncrs5", 
        "email": "anderson.c.rms2005@gmail.com" 
    }
)

@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    return response

app.include_router(address_enterprise_controller.router)
app.include_router(follow_enterprise_controller.router)
app.include_router(follow_controller.router)
app.include_router(application_controller.router)
app.include_router(address_user_controller.router)
app.include_router(vacancy_skill_controller.router)
app.include_router(vacancy_controller.router)
app.include_router(area_controller.router)
app.include_router(saved_search_controller.router)
app.include_router(review_enterprise_controller.router)
app.include_router(employee_enterprise_controller.router)
app.include_router(favorite_post_enterprise_controller.router)
app.include_router(post_enterprise_controller.router)
app.include_router(my_skill_controller.router)
app.include_router(skill_controller.router)
app.include_router(media_post_user_controller.router)
app.include_router(curriculum_controller.router)
app.include_router(enterprise_controller.router)
app.include_router(favorite_post_user_controller.router)
app.include_router(post_user_controller.router)
app.include_router(industry_controller.router)
app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(category_controller.router)
