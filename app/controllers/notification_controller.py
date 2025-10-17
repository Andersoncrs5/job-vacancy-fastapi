from datetime import datetime

from fastapi import APIRouter, status, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import NotificationEntity
from app.dependencies.service_dependency import *
from app.schemas.notification_schemas import NotificationOUT
from app.services.base.jwt_service_base import JwtServiceBase
from app.utils.filter.notification_filter import NotificationFilter
from app.utils.res.responses_http import *

URL = "/api/v1/notification"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Notifications"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Page[NotificationOUT],
)
async def get_all(
    filter: NotificationFilter = Depends(),
    notification_service: NotificationServiceProvider = Depends(get_notification_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        _all: Final[list[NotificationEntity]] = await notification_service.get_all(filter)

        return paginate(_all)
    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

@router.get(
    "/{noti_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[NotificationOUT],
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
    }
)
async def get(
    noti_id: int,
    notification_service = Depends(get_notification_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if noti_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        noti: Final = await notification_service.get_by_id(noti_id)
        if noti is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Notification not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out = noti.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Notification found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(out),
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

@router.delete(
    "/{noti_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody,
    responses={
        status.HTTP_404_NOT_FOUND: RESPONSE_404,
        status.HTTP_400_BAD_REQUEST: RESPONSE_400,
    }
)
async def delete(
    noti_id: int,
    notification_service: NotificationServiceProvider = Depends(get_notification_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if noti_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        noti: Final = await notification_service.get_by_id(noti_id)
        if noti is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Notification not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if user_id != noti.user_id:
            return ORJSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=dict(ResponseBody(
                    code=status.HTTP_403_FORBIDDEN,
                    message="You cannot to delete this notification",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await notification_service.delete(noti)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                message="Notification deleted with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        return ORJSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

add_pagination(router)