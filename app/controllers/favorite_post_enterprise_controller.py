from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from app.configs.db.database import FavoritePostEnterpriseEntity, UserEntity ,PostUserEntity, PostEnterpriseEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.post_enterprise_schemas import PostEnterpriseOUT
# from app.schemas.favorite_post_user_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/favorite-post-enterprise", 
    tags=["Favorite Post Enterprise"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()


@router.delete(
    "/{id}",
    response_model=ResponseBody[None],
    status_code=200,
    responses = {
        404 : RESPONSE_404,
        400: RESPONSE_400
    }
)
async def delete(
    id: int,
    favorite_posts_enterprise_service: FavoritePostEnterpriseServiceProvider = Depends(get_favorite_posts_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
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
        
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        post: Final[FavoritePostEnterpriseEntity | None] = await favorite_posts_enterprise_service.get_by_id(id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await favorite_posts_enterprise_service.delete(post)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Post removed with successfully",
                code=status.HTTP_200_OK,
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

@router.get(
    "/{user_id}",
    response_model=Page[PostEnterpriseOUT],
    status_code = 200,
    responses = {
        400: RESPONSE_400
    }
)
async def get_all(
    user_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    favorite_posts_enterprise_service: FavoritePostEnterpriseServiceProvider = Depends(get_favorite_posts_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if user_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
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
        jwt_service.valid_credentials(credentials)

        check = await user_service.exists_by_id(user_id)
        if check == False:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        all = await favorite_posts_enterprise_service.get_all_by_user_id_just_post(user_id)

        return paginate(all)
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
    '/{post_id}',
    response_model=ResponseBody[int],
    status_code=201,
    responses = {
        404: RESPONSE_404,
        400: RESPONSE_400
    }
)
async def create(
    post_id: int,
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    post_enterprise_service: PostEnterpriseServiceProvider = Depends(get_post_enterprise_service_provider_dependency),
    favorite_posts_enterprise_service: FavoritePostEnterpriseServiceProvider = Depends(get_favorite_posts_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
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

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        exists_post: Final[bool] = await favorite_posts_enterprise_service.exists_by_user_id_and_post_enterprise_id(user_id, post_id)
        if exists_post == True :
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="Post are already saved how favorite",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        user: Final[UserEntity | None] = await user_service.get_by_id(user_id)
        if user is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        post: Final[PostEnterpriseEntity | None] = await post_enterprise_service.get_by_id(post_id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody[None](
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        favorite_created: Final[FavoritePostEnterpriseEntity] = await favorite_posts_enterprise_service.add(post, user)

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[int](
                message="Post favorited with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=favorite_created.id,
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
    "/{post_id}/exists",
    response_model=ResponseBody[bool],
    status_code=200,
)
async def exists_favorite(
    post_id: int,
    favorite_posts_enterprise_service: FavoritePostEnterpriseServiceProvider = Depends(get_favorite_posts_enterprise_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody[None](
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
        
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        check = await favorite_posts_enterprise_service.exists_by_user_id_and_post_enterprise_id(user_id, post_id)

        message = "Favorite post already exists" if check else "Favorite post not exists"

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[bool](
                message=message,
                code=status.HTTP_200_OK,
                status=True,
                body=check,
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