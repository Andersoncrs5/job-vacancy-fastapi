from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import FavoritePostUserEntity, UserEntity, PostUserEntity
# from app.schemas.favorite_post_user_schemas import *
from app.dependencies.service_dependency import *
from app.schemas.post_user_schemas import PostUserOUT
from app.utils.enums.sum_red import ColumnUserMetricEnum, SumRedEnum, ColumnsPostUserMetricEnum
from app.utils.res.responses_http import *

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
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    favorite_posts_user_service: FavoritePostUserServiceProvider = Depends(get_favorite_posts_user_service_provider_dependency),
    post_user_metric_service: PostUserMetricServiceProvider = Depends(get_post_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_id <= 0:
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
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        exists_post: Final[bool] = await favorite_posts_user_service.exists_by_user_id_post_id(user_id, post_id)
        if exists_post:
            return ORJSONResponse(
                status_code=409,
                content=dict(ResponseBody(
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

        post_user: Final[PostUserEntity | None] = await post_user_service.get_by_id(post_id)
        if post_user is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Post user not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        favorite_created = await favorite_posts_user_service.add(post_user, user)
        await post_user_metric_service.update_metric(post_user.id, ColumnsPostUserMetricEnum.favorites_count, SumRedEnum.SUM)

        metric = await user_metric_service.get_by_id(user_id)
        await user_metric_service.update_metric(metric, ColumnUserMetricEnum.favorite_post_count, SumRedEnum.SUM)

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
    "/{user_id}",
    response_model=Page[PostUserOUT],
    status_code = 200,
    responses = {
        400: RESPONSE_400
    }
)
async def get_all_another_user(
    user_id: int,
    favorite_posts_user_service: FavoritePostUserServiceProvider = Depends(get_favorite_posts_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if user_id <= 0:
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
        jwt_service.valid_credentials(credentials)

        all = await favorite_posts_user_service.get_all_by_user_id_just_post(user_id)

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

@router.get(
    "/my",
    response_model=Page[PostUserOUT],
    status_code = 200
)
async def get_all(
    favorite_posts_user_service: FavoritePostUserServiceProvider = Depends(get_favorite_posts_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        all = await favorite_posts_user_service.get_all_by_user_id_just_post(user_id)

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


@router.delete(
    "/{id}",
    response_model=ResponseBody,
    status_code=200,
    responses = {
        404 : RESPONSE_404,
        400: RESPONSE_400
    }
)
async def delete(
    id: int,
    favorite_posts_user_service: FavoritePostUserServiceProvider = Depends(get_favorite_posts_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
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
                    version = 1,
                    path = None
                ))
            )

    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)
        
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        post: Final[FavoritePostUserEntity | None] = await favorite_posts_user_service.get_by_id(id)
        if post is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
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

        metric = await user_metric_service.get_by_id(user_id)
        await user_metric_service.update_metric(metric, ColumnUserMetricEnum.favorite_post_count, SumRedEnum.RED)
        await post_user_metric_service.update_metric(post.id, ColumnsPostUserMetricEnum.favorites_count,
                                                     SumRedEnum.RED)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
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
    if post_id <= 0:
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
        token: Final[str] = jwt_service.valid_credentials(credentials)
        
        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        check = await favorite_posts_user_service.exists_by_user_id_post_id(user_id, post_id)

        message = "Favorite post name already exists" if check else "Favorite post name not exists"

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