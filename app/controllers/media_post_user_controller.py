from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity, MediaPostUserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.enums.sum_red import SumRedEnum
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.media_post_user_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from app.utils.filter.post_user_filter import PostUserFilter
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/media-post-user", 
    tags=["MediaPostser"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
    )

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

