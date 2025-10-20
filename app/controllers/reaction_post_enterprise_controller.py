from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import ReactionPostEnterpriseEntity
from app.configs.db.enums import ReactionTypeEnum
from app.dependencies.service_dependency import *
from app.schemas.reaction_post_enterprise_schemas import ReactionPostEnterpriseWithRelationshipDTO, \
    CreateReactionPostEnterpriseDTO
from app.services.base.jwt_service_base import JwtServiceBase
from app.services.providers.reaction_post_enterprise_service_provider import ReactionPostEnterpriseServiceProvider
from app.services.providers.user_service_provider import UserServiceProvider
from app.utils.enums.sum_red import ColumnsPostEnterpriseMetricEnum, SumRedEnum
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

@router.get(
    "",
    response_model=Page[ReactionPostEnterpriseWithRelationshipDTO],
    status_code=status.HTTP_200_OK
)
async def get_all(
    user_id: int | None = None,
    post_enterprise_id: int | None = None,
    reaction_service: ReactionPostEnterpriseServiceProvider = Depends(get_reaction_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if (user_id and post_enterprise_id) or (not user_id and not post_enterprise_id):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="You must provide either user_id or post_enterprise_id, not both.",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        jwt_service.valid_credentials(creden=credentials)

        reacts: list[ReactionPostEnterpriseEntity] = await reaction_service.get_all(user_id, post_enterprise_id)

        return paginate(reacts)
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
                path=f'{URL}'
            ))
        )

@router.post(
    "",
    response_model=ResponseBody
)
async def create(
    dto: CreateReactionPostEnterpriseDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_enterprise_metric_service: PostEnterpriseMetricServiceProvider = Depends(get_post_enterprise_metric_service_provider_dependency),
    post_enterprise_service: PostUserServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    reaction_service: ReactionPostEnterpriseServiceProvider = Depends(get_reaction_post_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(creden=credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token=token)

        post = await post_enterprise_service.get_by_id(_id=dto.post_enterprise_id)
        if not post:
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        user = await user_service.exists_by_id(_id=user_id)
        if not user:
            return ORJSONResponse(
                status_code=404,
                content=dict(ResponseBody(
                    code=404,
                    message=f"User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        check = await reaction_service.get_by_user_id_and_post_enterprise_id(user_id=user_id, post_enterprise_id=dto.post_enterprise_id)

        if check and dto.reaction_type != check.reaction_type:

            reaction_updated = await reaction_service.toggle_reaction_type(check)

            if reaction_updated.reaction_type == ReactionTypeEnum.LIKE:
                await post_enterprise_metric_service.update_metric(
                    post.id,
                    ColumnsPostEnterpriseMetricEnum.reactions_dislike_count,
                    SumRedEnum.RED
                )

                await post_enterprise_metric_service.update_metric(
                    post.id,
                    ColumnsPostEnterpriseMetricEnum.reactions_like_count,
                    SumRedEnum.SUM
                )

            if reaction_updated.reaction_type == ReactionTypeEnum.DISLIKE:
                await post_enterprise_metric_service.update_metric(post.id, ColumnsPostEnterpriseMetricEnum.reactions_dislike_count, SumRedEnum.SUM)
                await post_enterprise_metric_service.update_metric(post.id, ColumnsPostEnterpriseMetricEnum.reactions_like_count, SumRedEnum.RED)

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    code=status.HTTP_200_OK,
                    message=f"Reaction updated with successfully",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        if check and dto.reaction_type == check.reaction_type:
            await reaction_service.delete(check)

            if dto.reaction_type == ReactionTypeEnum.LIKE:
                await post_enterprise_metric_service.update_metric(post.id, ColumnsPostEnterpriseMetricEnum.reactions_like_count, SumRedEnum.RED)
            else:
                await post_enterprise_metric_service.update_metric(post.id, ColumnsPostEnterpriseMetricEnum.reactions_dislike_count, SumRedEnum.RED)

            return ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody(
                    code=status.HTTP_200_OK,
                    message=f"Reaction removed with successfully",
                    status=True,
                    body=None,
                    timestamp=str(datetime.now()),
                    version=1,
                    path=None
                ))
            )

        await reaction_service.create(user_id=user_id, dto=dto)

        if dto.reaction_type == ReactionTypeEnum.LIKE:
            await post_enterprise_metric_service.update_metric(post.id,
                                                               ColumnsPostEnterpriseMetricEnum.reactions_like_count,
                                                               SumRedEnum.SUM)
        else:
            await post_enterprise_metric_service.update_metric(post.id,
                                                               ColumnsPostEnterpriseMetricEnum.reactions_dislike_count,
                                                               SumRedEnum.SUM)

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody(
                message="Reaction added with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

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

add_pagination(router)