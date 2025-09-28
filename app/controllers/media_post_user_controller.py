from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity, MediaPostUserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.enums.sum_red import SumRedEnum
from app.utils.filter.medias_post_user_filter import MediaPostUserFilter
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.media_post_user_schemas import *
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from app.utils.filter.post_user_filter import PostUserFilter
from datetime import datetime
from typing import Final, List

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/media-post-user", 
    tags=["MediaPostser"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.patch(
    "/{media_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[MediaPostUserOUT],
    responses={
        404: RESPONSE_404_POST_USER,
    }
)
async def update(
    media_id: int,
    dto: UpdateMediaPostUserDTO,
    media_post_user_service: MediaPostUserServiceProvider = Depends(get_media_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if media_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Post user id is required",
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

        media = await media_post_user_service.get_by_id(media_id)
        if media is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Media not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        media_updated = await media_post_user_service.update(media, dto)

        media_out = media_updated.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Media updated with successfully",
                code=200,
                status=True,
                body=dict(media_out),
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

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=Page[MediaPostUserOUT],
)
async def get_all(
    filter: MediaPostUserFilter = Depends(),
    media_post_user_service: MediaPostUserServiceProvider = Depends(get_media_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        all_entities: Final[List[MediaPostUserEntity]] = await media_post_user_service.get_all_filter(filter)

        return paginate(all_entities)

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
    "/{media_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[MediaPostUserOUT],
    responses={
        404: RESPONSE_404_POST_USER,
    }
)
async def get_by_id(
    media_id: int,
    media_post_user_service: MediaPostUserServiceProvider = Depends(get_media_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if media_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Post user id is required",
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

        media = await media_post_user_service.get_by_id(media_id)
        if media is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Media not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        media_out = media.to_out()

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[dict](
                message="Media found with successfully",
                code=200,
                status=True,
                body=dict(media_out),
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
    "/{media_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[MediaPostUserOUT],
    responses={
        404: RESPONSE_404_POST_USER,
    }
)
async def delete(
    media_id: int,
    media_post_user_service: MediaPostUserServiceProvider = Depends(get_media_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if media_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Post user id is required",
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

        media = await media_post_user_service.get_by_id(media_id)
        if media is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Media not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        await media_post_user_service.delete(media)

        return ORJSONResponse(
            status_code=200,
            content=dict(ResponseBody[None](
                message="Media deleted with successfully",
                code=200,
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

@router.post(
    "/{post_user_id}",
    status_code=201,
    response_model=ResponseBody[MediaPostUserOUT],
    responses={
        404: RESPONSE_404_POST_USER,
    }
)
async def create(
    post_user_id: int,
    dto: CreateMediaPostUserDTO,
    media_post_user_service: MediaPostUserServiceProvider = Depends(get_media_post_user_service_provider_dependency),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_user_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Post user id is required",
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

        check: Final[int] = await media_post_user_service.get_amount_by_post_id(post_user_id)
        if check >= 10:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="Limit to midia by post are 10",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        post_user: Final[bool] = await post_user_service.exists_by_id(post_user_id)
        if post_user == False:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post user not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        media_created = await media_post_user_service.create(post_user_id, dto)

        media_out = media_created.to_out()

        return ORJSONResponse(
            status_code=201,
            content=dict(ResponseBody[dict](
                message="Media created with successfully",
                code=201,
                status=True,
                body=dict(media_out),
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