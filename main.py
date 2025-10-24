from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from datetime import datetime

from app.configs.commands.command_linner import CommandLinner
from app.configs.logs.log_config import setup_logging
from app.controllers import (
    favorite_post_user_controller, auth_controller, user_controller,
    category_controller, post_user_controller, industry_controller,
    enterprise_controller, media_post_user_controller, curriculum_controller,
    skill_controller, my_skill_controller, post_enterprise_controller,
    favorite_post_enterprise_controller, employee_enterprise_controller,
    review_enterprise_controller, saved_search_controller, area_controller,
    vacancy_controller, vacancy_skill_controller, address_user_controller,
    address_enterprise_controller, application_controller, follow_controller,
    follow_enterprise_controller, reaction_post_user_controller, reaction_post_enterprise_controller,
    comment_post_user_controller, comment_post_enterprise_controller, favorite_comment_post_enterprise_controller,
    favorite_comment_post_user_controller, reaction_comment_post_user_controller,
    reaction_comment_post_enterprise_controller, enterprise_follows_user_controller, notification_controller,
    notification_enterprise_controller, adm_controller
)
from app.configs.db.database import get_db, engine, Base, AsyncSessionLocal
from contextlib import asynccontextmanager
from fastapi.responses import ORJSONResponse
from typing import Final
import structlog
import uuid

from app.repositories.providers.my_roles_repository_provider import MyRolesRepositoryProvider
from app.repositories.providers.roles_repository_provider import RolesRepositoryProvider
from app.repositories.providers.user_repository_provider import UserRepositoryProvider
from app.utils.res.response_body import ResponseBody

logger: Final[structlog.BoundLogger] = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # admin_service = KafkaAdmin(bootstrap_servers=[KAFKA_BROKER])
    # await asyncio.to_thread(admin_service.create_topics_from_file)

    async with AsyncSessionLocal() as db:
        user_repository = UserRepositoryProvider(db)
        role_repository = RolesRepositoryProvider(db)
        my_role_repository = MyRolesRepositoryProvider(db)
        cmd = CommandLinner(
            user_repository=user_repository,
            role_repository=role_repository,
            my_role_repository=my_role_repository,
        )

        await cmd.init_commands()

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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return ORJSONResponse(
        status_code=exc.status_code,
        content=dict(ResponseBody(
            code=exc.status_code,
            message=exc.detail.get("message") if isinstance(exc.detail, dict) else str(exc.detail),
            body=exc.detail.get("body") if isinstance(exc.detail, dict) else None,
            status=False,
            timestamp=str(datetime.now()),
            path=str(request.url.path),
            version=1
        ))
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(ResponseBody(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            body=str(exc),
            status=False,
            timestamp=str(datetime.now()),
            path=str(request.url.path),
            version=1
        ))
    )

@app.middleware("http")
async def add_request_id(request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    return response

app.include_router(adm_controller.router)
app.include_router(notification_controller.router)
app.include_router(notification_enterprise_controller.router)
app.include_router(enterprise_follows_user_controller.router)
app.include_router(reaction_comment_post_enterprise_controller.router)
app.include_router(favorite_comment_post_user_controller.router)
app.include_router(reaction_comment_post_user_controller.router)
app.include_router(favorite_comment_post_enterprise_controller.router)
app.include_router(comment_post_enterprise_controller.router)
app.include_router(reaction_post_enterprise_controller.router)
app.include_router(comment_post_user_controller.router)
app.include_router(reaction_post_user_controller.router)
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
