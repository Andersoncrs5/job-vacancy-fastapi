from typing import Final

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.utils.res.responses_http import *

URL = "/api/v1/area/reaction-post-enterprise"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Reaction Post Enterprise"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

add_pagination(router)