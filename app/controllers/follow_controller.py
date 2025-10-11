from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import FollowerRelationshipEntity
from app.dependencies.service_dependency import *
from app.schemas.follow_schemas import FollowOUT
from app.services.providers.follow_service_provider import FollowServiceProvider
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum
from app.utils.res.responses_http import *

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/follow",
    tags=["Follow"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    '/{followed_id}/exists',
    response_model=ResponseBody[bool],
    status_code=status.HTTP_200_OK
)
async def exists(
    followed_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    follow_service: FollowServiceProvider = Depends(get_follow_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if followed_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Id is required",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id = jwt_service.extract_user_id_v2(token)

        follow: Final = await follow_service.exists_by_follower_id_and_followed_id(user_id, followed_id)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[bool](
                code=status.HTTP_200_OK,
                message="",
                status=True,
                body=follow,
                timestamp=str(datetime.now()),
                version=1,
                path=None
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
    '/{followed_id}',
    response_model=ResponseBody,
    status_code=status.HTTP_200_OK
)
async def delete(
    followed_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    follow_service: FollowServiceProvider = Depends(get_follow_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if followed_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Id is required",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id = jwt_service.extract_user_id_v2(token)

        followed: Final = await user_service.get_by_id(followed_id)
        if not followed:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        follow: Final = await follow_service.get_by_follower_id_and_followed_id(user_id, followed_id)
        if not follow:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Follow not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await follow_service.delete(follow)

        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.followed_count, SumRedEnum.RED)
        await user_metric_service.update_metric_v2(followed_id, ColumnUserMetricEnum.follower_count, SumRedEnum.RED )

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                code=status.HTTP_200_OK,
                message=f"you unfollowed {followed.name}",
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
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

@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=Page[FollowOUT],
)
async def get_all(
    user_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    follow_service: FollowServiceProvider = Depends(get_follow_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if user_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Id is required",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user: Final = await user_service.exists_by_id(user_id)
        if not user:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        entities: Final[list[FollowerRelationshipEntity]] = await follow_service.get_all(user_id)

        return paginate(entities)
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

@router.post(
    '/{followed_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody,
)
async def create(
    followed_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    follow_service: FollowServiceProvider = Depends(get_follow_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if followed_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Id is required",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id = jwt_service.extract_user_id_v2(token)

        followed: Final = await user_service.get_by_id(followed_id)
        if not followed :
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        check = await follow_service.exists_by_follower_id_and_followed_id(user_id, followed_id)
        if check :
            return ORJSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=dict(ResponseBody(
                    code=status.HTTP_409_CONFLICT,
                    message=f"You already are following the {followed.name}",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await follow_service.create(user_id, followed_id)

        await user_metric_service.update_metric_v2(user_id,ColumnUserMetricEnum.followed_count,SumRedEnum.SUM)
        await user_metric_service.update_metric_v2(followed_id,ColumnUserMetricEnum.follower_count,SumRedEnum.SUM)

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody(
                code=status.HTTP_201_CREATED,
                message=f"You are following the {followed.name}",
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
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