from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import SkillEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.my_skill_schemas import *
from app.services.providers.skill_service_provider import SkillServiceProvider
from app.services.providers.my_skill_service_provider import MySkillServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime
from app.utils.filter.my_skill_filter import MySkillFilter
from app.configs.db.database import MySkillEntity
import json

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/review-enterprise", 
    tags=["Review Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()
