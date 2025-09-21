from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.configs.db.database import FavoritePostUserEntity, UserEntity ,PostUserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from app.utils.res.response_body import ResponseBody
from app.utils.res.responses_http import *
from app.schemas.favorite_post_user_schemas import *
from app.services.providers.user_service_provider import UserServiceProvider
from app.dependencies.service_dependency import *
from fastapi_pagination import Page, add_pagination, paginate
from datetime import datetime

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/favorite-post-user", 
    tags=["Favorite Post User"],
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
    favorite_posts_user_service: FavoritePostUserServiceProvider = Depends(get_favorite_posts_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if id is None or id <= 0:
        return JSONResponse(
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
        
        user_id: Final[int | None] = jwt_service.extract_user_id(token)
        if user_id is None or user_id <= 0:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody[None](
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        post: Final[FavoritePostUserEntity | None] = await favorite_posts_user_service.get_by_id(id)
        if post is None:
            return JSONResponse(
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

        await favorite_posts_user_service.delete(post)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                message="Post removed",
                code=status.HTTP_200_OK,
                status=True,
                body=None,
                timestamp=str(datetime.now()),
                version = 1,
                path = None
            ))
        )

    except Exception as e:
        return JSONResponse(
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
    favorite_posts_user_service: FavoritePostUserServiceProvider = Depends(get_favorite_posts_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        
        user_id: Final[int | None] = jwt_service.extract_user_id(token)
        if user_id is None or user_id <= 0:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=dict(ResponseBody[None](
                    code=status.HTTP_401_UNAUTHORIZED,
                    message="You are not authorized",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        check = await favorite_posts_user_service.exists_by_user_id_post_id(user_id, post_id)

        message = "Favorite post name already exists" if check else "Favorite post name not exists"

        return JSONResponse(
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
        return JSONResponse(
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