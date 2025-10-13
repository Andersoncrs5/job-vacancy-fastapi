from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import CommentPostEnterpriseEntity
from app.dependencies.service_dependency import *
from app.schemas.comment_post_enterprise_schemas import CommentPostEnterpriseOUT, CreateCommentPostEnterpriseDTO, \
    UpdateCommentPostEnterpriseDTO
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum, ColumnsPostEnterpriseMetricEnum, \
    ColumnsCommentPostEnterpriseMetricEnum
from app.utils.filter.comment_post_enterprise_filter import CommentPostEnterpriseFilter
from app.utils.res.responses_http import *

URL = "/api/v1/comment-post-enterprise"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Comment Post Enterprise"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    "/{id}",
    response_model=ResponseBody[CommentPostEnterpriseOUT],
    status_code=status.HTTP_200_OK
)
async def patch(
    id: int,
    dto: UpdateCommentPostEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    comment_service: CommentPostEnterpriseServiceProvider = Depends(get_comment_post_enterprise_service_provider_dependency),
    comment_enterprise_metric_service: CommentPostEnterpriseMetricServiceProvider = Depends(get_comment_post_enterprise_metric_service_provider_dependency),
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
        await comment_enterprise_metric_service.update_metric(comment.id,
                                                           ColumnsCommentPostEnterpriseMetricEnum.edited_count,
                                                           SumRedEnum.SUM)

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
    post_enterprise_metric_service: PostEnterpriseMetricServiceProvider = Depends(get_post_enterprise_metric_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    comment_service: CommentPostEnterpriseServiceProvider = Depends(get_comment_post_enterprise_service_provider_dependency),
    comment_enterprise_metric_service: CommentPostEnterpriseMetricServiceProvider = Depends(get_comment_post_enterprise_metric_service_provider_dependency),
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
        await post_enterprise_metric_service.update_metric(
            comment.post_enterprise_id,
            ColumnsPostEnterpriseMetricEnum.comments_count,
            SumRedEnum.RED
        )

        if comment.parent_comment_id is not None:
            await comment_enterprise_metric_service.update_metric(
                comment.parent_comment_id,
                ColumnsCommentPostEnterpriseMetricEnum.replies_count,
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
    response_model=ResponseBody[CommentPostEnterpriseOUT],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    comment_service: CommentPostEnterpriseServiceProvider = Depends(get_comment_post_enterprise_service_provider_dependency),
    comment_enterprise_metric_service: CommentPostEnterpriseMetricServiceProvider = Depends(get_comment_post_enterprise_metric_service_provider_dependency),
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

        await comment_enterprise_metric_service.update_metric(comment.id,
                                                              ColumnsCommentPostEnterpriseMetricEnum.views_count,
                                                              SumRedEnum.SUM)

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

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Page[CommentPostEnterpriseOUT],
)
async def get_all(
    filter: CommentPostEnterpriseFilter = Depends(),
    comment_service: CommentPostEnterpriseServiceProvider = Depends(get_comment_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)

        comments: list[CommentPostEnterpriseEntity] = await comment_service.get_all(filter)

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

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBody[CommentPostEnterpriseOUT]
)
async def create(
    dto: CreateCommentPostEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_enterprise_metric_service: PostEnterpriseMetricServiceProvider = Depends(get_post_enterprise_metric_service_provider_dependency),
    post_enterprise_service: PostUserServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    comment_service: CommentPostEnterpriseServiceProvider = Depends(get_comment_post_enterprise_service_provider_dependency),
    comment_enterprise_metric_service: CommentPostEnterpriseMetricServiceProvider = Depends(get_comment_post_enterprise_metric_service_provider_dependency),
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

        post = await post_enterprise_service.get_by_id(dto.post_enterprise_id)
        if not post:
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
        await comment_enterprise_metric_service.create(comment_created.id)

        if dto.parent_comment_id is not None:
            await comment_enterprise_metric_service.update_metric(dto.parent_comment_id, ColumnsCommentPostEnterpriseMetricEnum.replies_count, SumRedEnum.SUM)

        out = comment_created.to_out()

        out_dict = out.model_dump(by_alias=True)
        await user_metric_service.update_metric_v2(user_id, ColumnUserMetricEnum.comment_count, SumRedEnum.SUM)
        await post_enterprise_metric_service.update_metric(post.id,
                                                           ColumnsPostEnterpriseMetricEnum.comments_count,
                                                           SumRedEnum.SUM)

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

add_pagination(router)