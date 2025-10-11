from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi_pagination import Page, add_pagination, paginate

from app.configs.db.database import PostUserEntity, UserEntity, CategoryEntity
from app.dependencies.service_dependency import *
from app.schemas.post_user_schemas import *
from app.utils.enums.sum_red import SumRedEnum, ColumnUserMetricEnum
from app.utils.filter.post_user_filter import PostUserFilter
from app.utils.res.responses_http import *

router: Final[APIRouter] = APIRouter(
    prefix="/api/v1/post-user", 
    tags=["PostUser"],
    responses={
        500: RESPONSE_500,
        status.HTTP_401_UNAUTHORIZED: RESPONSE_401,
    },
    deprecated=False,
)

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.delete(
    "/{post_user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody,
    responses={
        404: RESPONSE_404_POST_USER,
    }
)
async def delete(
    post_user_id: int,
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_user_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
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

        post_user: Final[PostUserEntity | None] = await post_user_service.get_by_id(post_user_id)
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

        await post_user_service.delete(post_user)

        category = await category_service.get_by_id(post_user.category_id)
        if category is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )

        await category_service.sum_red_post_count(category, SumRedEnum.RED)

        metric_user = await user_metric_service.get_by_id(user_id)
        await user_metric_service.update_metric(metric_user, ColumnUserMetricEnum.post_count, SumRedEnum.RED)

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody(
                message="Post deleted with successfully",
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
    "/{post_user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[PostUserOUT],
    responses={
        404: RESPONSE_404_POST_USER,
    }
)
async def get(
    post_user_id: int,
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_user_id <= 0:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(ResponseBody(
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

        post_user: Final[PostUserEntity | None] = await post_user_service.get_by_id(post_user_id)
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
        
        post_user_out: Final[PostUserOUT] = post_user.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Post found with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(post_user_out),
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

@router.put(
    '/{post_user_id}',
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[PostUserOUT],
    responses={
        404: RESPONSE_404,
    }
)
async def update(
    post_user_id: int,
    dto: UpdatePostUserDTO,
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if post_user_id <= 0:
        return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
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

        post_user: Final[PostUserEntity | None] = await post_user_service.get_by_id(post_user_id)
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
        
        post_user_updated: Final[PostUserEntity] = await post_user_service.update(post_user, dto)

        post_user_out: Final[PostUserOUT] = post_user_updated.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[dict](
                message="Post updated with successfully",
                code=status.HTTP_200_OK,
                status=True,
                body=dict(post_user_out),
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
    '',
    status_code=status.HTTP_200_OK,
    response_model=Page[PostUserOUT],
    )
async def get_all(
    filter: PostUserFilter = Depends(),
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id: Final[int] = jwt_service.extract_user_id_v2(token)

        categories: Final[list[PostUserEntity]] = await post_user_service.get_all_filter(filter)

        return paginate(categories)

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
    '/{category_id}',
    response_model=ResponseBody[PostUserOUT],
    status_code=status.HTTP_201_CREATED,
    responses={
        404: RESPONSE_404,
    }
)
async def create(
    category_id: int,
    dto: CreatePostUserDTO,
    post_user_service: PostUserServiceProvider = Depends(get_post_user_service_provider_dependency),
    user_metric_service: UserMetricServiceProvider = Depends(get_user_metric_service_provider_dependency),
    user_service: UserServiceProvider = Depends(get_user_service_provider_dependency),
    category_service: CategoryServiceProvider = Depends(get_category_service_provider_dependency),
    jwt_service: JwtServiceBase = Depends(get_jwt_service_dependency),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    if category_id <= 0:
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

        category: Final[CategoryEntity | None] = await category_service.get_by_id(category_id)
        if category is None:
            return ORJSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=dict(ResponseBody(
                    code=status.HTTP_404_NOT_FOUND,
                    message="Category not found",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  
        
        if not category.is_active:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=dict(ResponseBody(
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Category are not actived",
                    status=False,
                    body=None,
                    timestamp=str(datetime.now()),
                    version = 1,
                    path = None
                ))
            )  

        post_user_created: Final[PostUserEntity] = await post_user_service.create(user, category, dto)

        await category_service.sum_red_post_count(category, SumRedEnum.SUM)

        metric_user = await user_metric_service.get_by_id(user_id)
        await user_metric_service.update_metric(metric_user, ColumnUserMetricEnum.post_count, SumRedEnum.SUM)

        post_user_out = post_user_created.to_out()

        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=dict(ResponseBody[dict](
                message="Post created with successfully",
                code=status.HTTP_201_CREATED,
                status=True,
                body=dict(post_user_out),
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