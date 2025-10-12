from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import EnterpriseEntity
from app.dependencies.service_dependency import *
from app.schemas.enterprise_follows_user_schemas import EnterpriseFollowsUserOUT
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum, ColumnEnterpriseMetricEnum
from app.utils.filter.enterprise_follows_user_filter import EnterpriseFollowsUserFilter
from app.utils.res.responses_http import *

URL = "/api/v1/enterprise-follow-user"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Enterprise Follow User"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "/exists",
    response_model=ResponseBody[bool],
    status_code=status.HTTP_200_OK
)
async def exists(
    followed_user_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    enterprise_follow_service: EnterpriseFollowsUserServiceProvider = Depends(get_enterprise_follows_user_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id = jwt_service.extract_user_id_v2(token)

        enterprise: Final = await enterprise_service.get_by_user_id(user_id)
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

        follow = await enterprise_follow_service.exists_by_enterprise_id_and_user_id(enterprise.id, followed_user_id)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[bool](
                code=status.HTTP_200_OK,
                message=f"",
                status=True,
                body=follow,
                timestamp=str(datetime.now()),
                version=1,
                path=None,
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
                path=f'{URL}/{followed_user_id}'
            ))
        )

@router.get(
    "",
    response_model=Page[EnterpriseFollowsUserOUT],
)
async def get_all(
    filter: EnterpriseFollowsUserFilter = Depends(),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    enterprise_follow_service: EnterpriseFollowsUserServiceProvider = Depends(get_enterprise_follows_user_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        user_id = jwt_service.extract_user_id_v2(token)

        follows = await enterprise_follow_service.get_all(filter)

        return paginate(follows)

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
                path=None
            ))
        )

@router.post(
    "/toggle/{followed_user_id}",
    response_model=ResponseBody,
)
async def toggle(
    followed_user_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    enterprise_service: EnterpriseServiceProvider = Depends(get_enterprise_service_provider_dependency),
    enterprise_metric_service: EnterpriseMetricServiceProvider = Depends(get_enterprise_metric_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    enterprise_follow_service: EnterpriseFollowsUserServiceProvider = Depends(get_enterprise_follows_user_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if followed_user_id <= 0:
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

        followed_user: Final = await user_service.get_by_id(followed_user_id)
        if not followed_user:
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

        enterprise: EnterpriseEntity | None = await enterprise_service.get_by_user_id(user_id)
        if enterprise is None:
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

        follow = await enterprise_follow_service.get_by_enterprise_id_and_user_id(enterprise.id, followed_user_id)

        if follow :
            await enterprise_metric_service.update_metric(
                enterprise.id,
                ColumnEnterpriseMetricEnum.followed_count,
                SumRedEnum.RED
            )

            await user_metric_service.update_metric_v2(
                followed_user_id,
                ColumnUserMetricEnum.follower_count,
                SumRedEnum.RED
            )

            await enterprise_follow_service.delete(follow)

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    code=status.HTTP_200_OK,
                    message=f"You unfollowed the user {followed_user.name}",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await enterprise_follow_service.create(enterprise.id, followed_user_id)

        await enterprise_metric_service.update_metric(
            enterprise.id,
            ColumnEnterpriseMetricEnum.followed_count,
            SumRedEnum.SUM
        )

        await user_metric_service.update_metric_v2(
            followed_user_id,
            ColumnUserMetricEnum.follower_count,
            SumRedEnum.SUM
        )

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody(
                code=status.HTTP_201_CREATED,
                message=f"You are following the user {followed_user.name}",
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
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
                path=f'{URL}/{followed_user_id}'
            ))
        )

add_pagination(router)