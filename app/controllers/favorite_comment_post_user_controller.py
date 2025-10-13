from datetime import datetime
from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.dependencies.service_dependency import *
from app.schemas.favorite_comment_post_user_schemas import FavoriteCommentPostUserOUT
from app.services.base.jwt_service_base import JwtServiceBase
from app.services.providers.user_service_provider import UserServiceProvider
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum, ColumnsCommentPostUserMetricEnum
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import RESPONSE_500, RESPONSE_401

URL = "/api/v1/favorite-comment-post-user"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Favorite Comment Post User"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "",
    response_model=Page[FavoriteCommentPostUserOUT],
    status_code=status.HTTP_200_OK
)
async def get_all(
    user_id: int | None = None,
    comment_id: int | None = None,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    favorite_comment_service: FavoriteCommentPostUserServiceProvider = Depends(get_favorite_comment_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        if (user_id and comment_id) or (not user_id and not comment_id):
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="You must provide either user_id or comment_id, not both.",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if user_id:
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

        if comment_id:
            comment = await comment_service.get_by_id(comment_id)
            if not comment:
                return ORJSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=dict(ResponseBody(
                        code=status.HTTP_404_NOT_FOUND,
                        message="Comment not found",
                        status=False,
                        body=None,
                        timestamp=str(datetime.now()),
                        version=1,
                        path=None
                    ))
                )

        token: Final[str] = jwt_service.valid_credentials(credentials)

        favors = await favorite_comment_service.get_all(user_id, comment_id)

        return paginate(favors)
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
    '/toggle-favorite/{comment_id}',
    response_model=ResponseBody,
)
async def toggle(
    comment_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    comment_post_user_metric_service: CommentPostUserMetricServiceProvider = Depends(get_comment_post_user_metric_service_provider_dependency),
    favorite_comment_service: FavoriteCommentPostUserServiceProvider = Depends(get_favorite_comment_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if comment_id <= 0:
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
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

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

        comment = await comment_service.exists_by_id(comment_id)
        if not comment:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Comment not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        favor = await favorite_comment_service.get_by_user_id_and_comment_user_id(user_id, comment_id)

        if favor:
            await favorite_comment_service.delete(favor)

            await comment_post_user_metric_service.update_metric(
                comment_id,
                ColumnsCommentPostUserMetricEnum.favorites_count,
                SumRedEnum.RED
            )

            await user_metric_service.update_metric_v2(
                user_id,
                ColumnUserMetricEnum.favorite_comment_count,
                SumRedEnum.RED
            )

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    code=status.HTTP_200_OK,
                    message="Comment removed with favorite",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await favorite_comment_service.create(user_id, comment_id)
        await user_metric_service.update_metric_v2(
            user_id,
            ColumnUserMetricEnum.favorite_comment_count,
            SumRedEnum.SUM
        )

        await comment_post_user_metric_service.update_metric(
            comment_id,
            ColumnsCommentPostUserMetricEnum.favorites_count,
            SumRedEnum.SUM
        )

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody(
                code=status.HTTP_201_CREATED,
                message="Comment saved with favorite",
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