from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.dependencies.service_dependency import *
from app.schemas.follow_enterprise_schemas import FollowEnterpriseOUT
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum
from app.utils.res.responses_http import *

URL = "/api/v1/follow-enterprise"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["FollowEnterprise"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.delete(
    "/{enterprise_id}",
    response_model=ResponseBody[bool],
    status_code=status.HTTP_200_OK
)
async def delete(
    enterprise_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    follow_enterprise_service: FollowEnterpriseServiceProvider = Depends(get_follow_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if not enterprise_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id = jwt_service.extract_user_id_v2(token)

        entity = await follow_enterprise_service.get_by_user_id_and_enterprise_id(user_id, enterprise_id)
        if not entity:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="You are not following this enterprise",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await follow_enterprise_service.delete(entity)

        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.followed_count, SumRedEnum.RED )

        # await user_metric_service.update_metric_v2(enterprise_id, ColumnUserMetricEnum.enterprise_follower_count, SumRedEnum.RED )

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                code=status.HTTP_200_OK,
                message=f"",
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=f'URL/{enterprise_id}'
            ))
        )

    except Exception as e:
        print('error: ', e)
        return ORJSONResponse(
            status_code=500,
            content=dict(ResponseBody[Any](
                code=500,
                message="Error in server! Please try again later",
                status=False,
                body=str(e),
                timestamp=str(datetime.now()),
                version=1,
                path=f'URL/{enterprise_id}'
            ))
        )

@router.get(
    "/{enterprise_id}/exists",
    response_model=ResponseBody[bool],
    status_code=status.HTTP_200_OK
)
async def exists(
    enterprise_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    follow_enterprise_service: FollowEnterpriseServiceProvider = Depends(get_follow_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if not enterprise_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="Id is required",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id = jwt_service.extract_user_id_v2(token)

        check = await follow_enterprise_service.exists_by_user_id_and_enterprise_id(user_id, enterprise_id)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[bool](
                code=status.HTTP_200_OK,
                message=f"",
                status=True,
                body=check,
                timestamp=str(datetime.now()),
                version=1,
                path=f'URL/{enterprise_id}'
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
                version=1,
                path=f'URL/{enterprise_id}'
            ))
        )

@router.get(
    "",
    response_model=Page[FollowEnterpriseOUT],
    status_code=200
)
async def get_all(
    user_id: int | None = None,
    enterprise_id: int | None = None,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    follow_enterprise_service: FollowEnterpriseServiceProvider = Depends(get_follow_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if (user_id and enterprise_id) or (not user_id and not enterprise_id):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="You must provide either user_id or enterprise_id, not both.",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        followers = await follow_enterprise_service.get_all_filtered(user_id, enterprise_id)

        return paginate(followers)
    except Exception as e:
        return ORJSONResponse(
            status_code=500,
            content=dict(ResponseBody[Any](
                code=500,
                message="Error in server! Please try again later",
                status=False,
                body=str(e),
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

@router.post(
    '/{enterprise_id}',
    response_model=ResponseBody,
    status_code=status.HTTP_200_OK
)
async def follow(
    enterprise_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    follow_enterprise_service: FollowEnterpriseServiceProvider = Depends(get_follow_enterprise_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if enterprise_id <= 0:
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
        user = await user_service.get_by_id(user_id)
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

        enterprise = await enterprise_service.get_by_id(enterprise_id)
        if not enterprise:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Enterprise not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        check_exists = await follow_enterprise_service.exists_by_user_id_and_enterprise_id(user_id, enterprise_id)
        if check_exists:
            return ORJSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=dict(ResponseBody(
                    code=status.HTTP_409_CONFLICT,
                    message=f"You already are following the enterprise: {enterprise.name}",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if enterprise.user_id == user_id:
            return ORJSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=dict(ResponseBody(
                    code=status.HTTP_403_FORBIDDEN,
                    message="You cannot to follow your enterprise!",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await follow_enterprise_service.create(user_id, enterprise_id)
        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.followed_count, SumRedEnum.SUM)

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody(
                code=status.HTTP_201_CREATED,
                message=f"You are following the enterprise {enterprise.name}",
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
                version=1,
                path=None
            ))
        )

add_pagination(router)