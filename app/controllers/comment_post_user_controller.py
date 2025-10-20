from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.enums import NotificationTypeEnum
from app.dependencies.service_dependency import *
from app.schemas.comment_post_user_schemas import CommentPostUserOUT, CreateCommentPostUserDTO, UpdateCommentPostUserDTO
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum, ColumnsPostUserMetricEnum, \
    ColumnsCommentPostUserMetricEnum
from app.utils.filter.comment_post_user_filter import CommentPostUserFilter
from app.utils.res.responses_http import *

URL = "/api/v1/comment-post-user"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Comment Post User"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "/{id}/metric",
    response_model=ResponseBody[CommentPostUserOUT],
    status_code=status.HTTP_200_OK
)
async def get_by_id_metric(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    notification_service: NotificationEventServiceProvider = Depends(get_notification_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    comment_post_user_metric_service: CommentPostUserMetricServiceProvider = Depends(get_comment_post_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
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

        comment = await comment_service.get_by_id(id)
        if comment is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Comment not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        metric = await comment_post_user_metric_service.get_by_id(id)

        out_dict = metric.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Comment metric found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(out_dict),
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error :', e)
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

@router.patch(
    "/{id}",
    response_model=ResponseBody[CommentPostUserOUT],
    status_code=status.HTTP_200_OK
)
async def patch(
    id: int,
    dto: UpdateCommentPostUserDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    comment_post_user_metric_service: CommentPostUserMetricServiceProvider = Depends(get_comment_post_user_metric_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
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

        comment = await comment_service.get_by_id(id)
        if comment is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Comment not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        comment_updated = await comment_service.update(comment, dto)

        out = comment_updated.to_out()
        out_dict = out.model_dump(by_alias=True)

        await comment_post_user_metric_service.update_metric(
            comment_updated.id,
            ColumnsCommentPostUserMetricEnum.edited_count,
            SumRedEnum.SUM
        )

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Comment updated with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=out_dict,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error :', e)
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

@router.delete(
    "/{id}",
    response_model=ResponseBody,
    status_code=status.HTTP_200_OK
)
async def delete(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    comment_post_user_metric_service: CommentPostUserMetricServiceProvider = Depends(get_comment_post_user_metric_service_provider_dependency),
    post_user_metric_service: PostUserMetricServiceProvider = Depends(get_post_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
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

        comment = await comment_service.get_by_id(id)
        if comment is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Comment not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await comment_service.delete(comment)
        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.comment_count, SumRedEnum.RED)
        await post_user_metric_service.update_metric(comment.post_user_id, ColumnsPostUserMetricEnum.comments_count, SumRedEnum.RED)

        if comment.parent_comment_id is not None:
            await comment_post_user_metric_service.update_metric(
                comment.parent_comment_id,
                ColumnsCommentPostUserMetricEnum.replies_count,
                SumRedEnum.RED
            )

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                message="Comment deleted with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error :', e)
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

@router.get(
    "/{id}",
    response_model=ResponseBody[CommentPostUserOUT],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    comment_post_user_metric_service: CommentPostUserMetricServiceProvider = Depends(get_comment_post_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
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

        comment = await comment_service.get_by_id(id)
        if comment is None :
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Comment not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out = comment.to_out()

        out_dict = out.model_dump(by_alias=True)
        await comment_post_user_metric_service.update_metric(comment.id, ColumnsCommentPostUserMetricEnum.views_count, SumRedEnum.SUM)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Comment found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=out_dict,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error :', e)
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
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBody[CommentPostUserOUT]
)
async def create(
    dto: CreateCommentPostUserDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    notification_service: NotificationEventServiceProvider = Depends(get_notification_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    comment_post_user_metric_service: CommentPostUserMetricServiceProvider = Depends(get_comment_post_user_metric_service_provider_dependency),
    post_user_metric_service: PostUserMetricServiceProvider = Depends(get_post_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
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
                    version = 1,
                    path = None
                ))
            )

        post_user = await post_user_service.get_by_id(dto.post_user_id)
        if not post_user:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if dto.parent_comment_id :
            exists_comment = await comment_service.exists_by_id(dto.parent_comment_id)

            if not exists_comment:
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

        comment_created = await comment_service.create(user_id, dto)

        if dto.parent_comment_id is not None:
            await comment_post_user_metric_service.update_metric(
                dto.parent_comment_id,
                ColumnsCommentPostUserMetricEnum.replies_count,
                SumRedEnum.SUM
            )

        out = comment_created.to_out()
        await comment_post_user_metric_service.create(comment_created.id)

        out_dict = out.model_dump(by_alias=True, exclude_none=True)
        await user_metric_service.update_metric_v2(
            user_id,
            ColumnUserMetricEnum.comment_count,
            SumRedEnum.SUM
        )

        await post_user_metric_service.update_metric(
            dto.post_user_id,
            ColumnsPostUserMetricEnum.comments_count,
            SumRedEnum.SUM
        )

        await notification_service.notify_user_about(
            entity_id=comment_created.id,
            actor_id=user_id,
            data={
                "user_name": user.name,
            },
            _type=NotificationTypeEnum.NEW_COMMENT
        )

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Comment created with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=out_dict,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error :', e)
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

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Page[CommentPostUserOUT],
)
async def get_all(
    filter: CommentPostUserFilter = Depends(),
    comment_service: CommentPostUserServiceProvider = Depends(get_comment_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)

        comments = await comment_service.get_all(filter)

        return paginate(comments)
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