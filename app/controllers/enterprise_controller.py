from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.configs.db.database import EnterpriseEntity, UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.enterprise_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from app.utils.filter.enterprise_filter import EnterpriseFilter
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/enterprise", 
    tags=["Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
    )

bearer_scheme: Final[HTTPBearer] = HTTPBearer()




add_pagination(router)