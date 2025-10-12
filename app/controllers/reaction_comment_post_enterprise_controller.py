from datetime import datetime
from typing import Final, Any

from fastapi import APIRouter, status, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.enums import ReactionTypeEnum
from app.dependencies.service_dependency import *
from app.schemas.reaction_comment_post_enterprise_schemas import (
    CreateReactionCommentPostEnterpriseDTO,
    ReactionCommentPostEnterpriseOUT
)
from app.utils.enums.sum_red import ColumnsCommentPostEnterpriseMetricEnum, SumRedEnum
from app.utils.filter.reaction_comment_post_enterprise_filter import ReactionCommentPostEnterpriseFilter

from app.utils.res.responses_http import *

URL = "/api/v1/area/reaction-comment-enterprise"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Reaction Comment Enterprise"],
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
    response_model=Page[ReactionCommentPostEnterpriseOUT],
)
async def get_all(
    filter: ReactionCommentPostEnterpriseFilter = Depends(),
    reaction_service: ReactionCommentPostEnterpriseServiceProvider = Depends(get_reaction_comment_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        jwt_service.valid_credentials(credentials)

        reacts = await reaction_service.get_all(filter)

        return paginate(reacts)
    except Exception as e:
        print(e)
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
    response_model=ResponseBody,
)
async def toggle(
    dto: CreateReactionCommentPostEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    comment_enterprise_metric_service: CommentPostEnterpriseMetricServiceProvider = Depends(get_comment_post_enterprise_metric_service_provider_dependency),
    reaction_service: ReactionCommentPostEnterpriseServiceProvider = Depends(get_reaction_comment_post_enterprise_service_provider_dependency),
    comment_service: CommentPostEnterpriseServiceProvider = Depends(get_comment_post_enterprise_service_provider_dependency),
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
                    version=1,
                    path=None
                ))
            )

        comment = await comment_service.get_by_id(dto.comment_enterprise_id)
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

        react = await reaction_service.get_by_user_id_and_comment_enterprise_id(user_id, dto.comment_enterprise_id)

        if react and react.reaction_type != dto.reaction_type:
            reaction_updated = await reaction_service.toggle_reaction_type(react)

            if reaction_updated.reaction_type == ReactionTypeEnum.LIKE:
                await comment_enterprise_metric_service.update_metric(
                    comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_dislike_count, SumRedEnum.RED
                )
                await comment_enterprise_metric_service.update_metric(
                    comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_like_count, SumRedEnum.SUM
                )

            elif reaction_updated.reaction_type == ReactionTypeEnum.DISLIKE:
                await comment_enterprise_metric_service.update_metric(
                    comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_like_count, SumRedEnum.RED
                )
                await comment_enterprise_metric_service.update_metric(
                    comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_dislike_count, SumRedEnum.SUM
                )

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    code=status.HTTP_200_OK,
                    message="Reaction type changed successfully",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        if react and react.reaction_type == dto.reaction_type:
            await reaction_service.delete(react)

            if dto.reaction_type == ReactionTypeEnum.LIKE:
                await comment_enterprise_metric_service.update_metric(
                    comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_like_count, SumRedEnum.RED
                )
            else:
                await comment_enterprise_metric_service.update_metric(
                    comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_dislike_count, SumRedEnum.RED
                )

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    code=status.HTTP_200_OK,
                    message="Reaction removed with successfully",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await reaction_service.create(user_id, dto)

        if dto.reaction_type == ReactionTypeEnum.LIKE:
            await comment_enterprise_metric_service.update_metric(
                comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_like_count, SumRedEnum.SUM
            )
        else:
            await comment_enterprise_metric_service.update_metric(
                comment.id, ColumnsCommentPostEnterpriseMetricEnum.reactions_dislike_count, SumRedEnum.SUM
            )

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody(
                code=status.HTTP_201_CREATED,
                message="Reaction created with successfully",
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


add_pagination(router)
