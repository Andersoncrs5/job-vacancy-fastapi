from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import VacancyEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.vacancy_schemas import *
from app.services.providers.vacancy_service_provider import VacancyServiceProvider
from app.services.providers.vacancy_skill_service_provider import VacancySkillServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime
import uuid

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/vacancy-skill", 
    tags=["Vacancy"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

add_pagination(router)