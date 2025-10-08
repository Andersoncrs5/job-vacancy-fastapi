from datetime import datetime
from typing import Final

from fastapi import APIRouter, status, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.dependencies.service_dependency import *
from app.schemas.reaction_post_user_schemas import CreateReactionPostUserDTO, ReactionPostUserOUT, \
    ReactionPostUserWithRelationshipOUT
from app.services.base.jwt_service_base import JwtServiceBase
from app.services.base.reaction_post_user_service_provider import ReactionPostUserServiceProvider
from app.services.providers.post_user_service_provider import PostUserServiceProvider
from app.services.providers.user_service_provider import UserServiceProvider
from app.utils.res.responses_http import *

URL = "/api/v1/area/reaction-post-user"

router: Final[APIRouter] = APIRouter(
    prefix=URL,
    tags=["Reaction Post User"],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "",
    response_model=Page[ReactionPostUserWithRelationshipOUT],
    status_code=status.HTTP_200_OK
)
async def get_all(
    user_id: int | None = None,
    post_user_id: int | None = None,
    reaction_service: ReactionPostUserServiceProvider = Depends(get_reaction_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if (user_id and post_user_id) or (not user_id and not post_user_id):
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
                code=status.HTTP_400_BAD_REQUEST,
                message="You must provide either user_id or post_user_id, not both.",
                status=False,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    try:
        jwt_service.valid_credentials(creden=credentials)

        reacts = await reaction_service.get_all(user_id, post_user_id)

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
    "/toggle",
    response_model=ResponseBody,
    status_code=status.HTTP_201_CREATED
)
async def create(
    dto: CreateReactionPostUserDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    reaction_service: ReactionPostUserServiceProvider = Depends(get_reaction_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(creden=credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token=token)

        post = await post_user_service.exists_by_id(id=dto.post_user_id)
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

        user = await user_service.exists_by_id(id=user_id)
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

        check = await reaction_service.get_by_user_id_and_post_user_id(user_id=user_id, post_user_id=dto.post_user_id)
        if check and dto.reaction_type != check.reaction_type:

            await reaction_service.toggle_reaction_type(check)

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

@router.get(
    "/{post_user_id}",
    response_model=ResponseBody[ReactionPostUserOUT],
    status_code=status.HTTP_200_OK
)
async def get(
    post_user_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    reaction_service: ReactionPostUserServiceProvider = Depends(get_reaction_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_user_id <= 0:
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
        token: Final[str] = jwt_service.valid_credentials(creden=credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token=token)

        post = await post_user_service.exists_by_id(id=post_user_id)
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

        react = await reaction_service.get_by_user_id_and_post_user_id(user_id=user_id, post_user_id=post_user_id)
        if not react:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message=f"Reaction not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        out = react.to_out_simple()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Reaction found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(out),
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error is', e)
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
    "/{post_user_id}",
    response_model=ResponseBody,
    status_code=status.HTTP_200_OK
)
async def delete(
    post_user_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    reaction_service: ReactionPostUserServiceProvider = Depends(get_reaction_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_user_id <= 0:
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
        token: Final[str] = jwt_service.valid_credentials(creden=credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token=token)

        post = await post_user_service.exists_by_id(id=post_user_id)
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

        react = await reaction_service.get_by_user_id_and_post_user_id(user_id=user_id, post_user_id=post_user_id)
        if not react:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message=f"Reaction not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await reaction_service.delete(react)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                message="Reaction deleted with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version=1,
                path=None
            ))
        )

    except Exception as e:
        print('Error is', e)
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
    status_code=status.HTTP_201_CREATED
)
async def create(
    dto: CreateReactionPostUserDTO,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    reaction_service: ReactionPostUserServiceProvider = Depends(get_reaction_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(creden=credentials)
        user_id: Final[int] = jwt_service.extract_user_id_v2(token=token)

        post = await post_user_service.exists_by_id(id=dto.post_user_id)
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

        user = await user_service.exists_by_id(id=user_id)
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

        check = await reaction_service.exists_by_user_id_and_post_user_id(user_id=user_id, post_user_id=dto.post_user_id)
        if check:
            return ORJSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=dict(ResponseBody(
                    code=status.HTTP_409_CONFLICT,
                    message=f"You have already reacted to this post",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await reaction_service.create(user_id=user_id, dto=dto)

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